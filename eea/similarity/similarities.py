""" similarities module
"""
import os
import datetime
import json
import logging
from collections import OrderedDict
import pytz
from zope.interface import Interface
from zope.component.hooks import getSite
from zope.component import queryUtility, queryAdapter
from Products.Five import BrowserView
from gensim import corpora, models, similarities
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from stemming.porter2 import stem
from eea.similarity.interfaces import IEEASimilaritySettings
from eea.similarity.async import IAsyncService
try:
    from eea.versions.interfaces import IGetVersions
except ImportError:
    class IGetVersions(Interface):
        """ No versioning """

MAX_DIFFERENCE = 0.1
SUGGESTIONS_PATH = os.environ.get('EEASIMILARITY_PATH',
                   os.environ.get('EEASUGGESTIONS_PATH', '/tmp'))

logger = logging.getLogger('eea.similarity')


def get_gensim_data():
    """ load the gensim data stored on disk """
    dictionary = corpora.Dictionary.load(SUGGESTIONS_PATH + '/dictionary.dict')
    corpus = corpora.MmCorpus(SUGGESTIONS_PATH + '/corpus.mm')
    lsi = models.LsiModel.load(SUGGESTIONS_PATH + '/lsi.lsi')
    index = similarities.MatrixSimilarity.load(SUGGESTIONS_PATH +
                                               '/index.index')
    return dictionary, corpus, lsi, index


class Suggestions(BrowserView):
    """ Suggestions class """

    def reference_threshold(self, length):
        """ return the reference threshold """
        settings = IEEASimilaritySettings(self.context).settings
        if length > 4:
            return float(settings.threshold2)
        return float(settings.threshold1)

    def __call__(self):
        """ returns a json with candidates of duplication
        """
        lang = getattr(self.context, 'getLanguage', lambda: 'en')
        if lang() != 'en':
            # suggestions only work for English
            return
        settings = IEEASimilaritySettings(self.context).settings
        max_difference = float(settings.max_difference) or MAX_DIFFERENCE
        equiv_types = []
        if settings.equivalent_content_types:
            equiv_types = [equiv_set.lower().replace(' ', '').split(',')
                           for equiv_set in settings.equivalent_content_types]
        max_suggestions = settings.number_of_suggestions or 5
        min_words = settings.min_words or 3
        catalog = getSite().portal_catalog
        candidates = OrderedDict()
        title = self.request.get('title')
        words = [word for word in simple_preprocess(title, deacc=True)
                 if not settings.remove_stopwords or word not in STOPWORDS]
        all_content_types = self.request.get('all_content_types')
        portal_type = self.request.get('portal_type')
        equivs = []
        for equiv_set in equiv_types:
            if portal_type in equiv_set:
                equivs.extend(equiv_set)
        if not equivs:
            equivs = [portal_type]

        if len(words) < min_words:
            return json.dumps(candidates)

        dictionary, corpus, lsi, index = get_gensim_data()
        vec_bow = dictionary.doc2bow([stem(word) for word in words])
        vec_lsi = lsi[vec_bow]
        sims = index[vec_lsi]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        previous_note = 0
        threshold = float(
            self.request.get('threshold',
                             self.reference_threshold(len(words))))
        for sim in sims:
            if sim[1] < threshold or (
                    previous_note - sim[1] > max_difference):
                # if the difference in similarity is big,
                # next candidates are no longer interesting
                break
            previous_note = sim[1]

            for word_id in corpus[sim[0]]:
                if len(dictionary[word_id[0]].replace('-', '')) == 32:
                    uid = dictionary[word_id[0]]
                    break
            try:
                brain = catalog({'UID': [uid, uid.upper()]})[0]
            except NameError as err:
                logger.warn('Catalog UID not found: %s', err)
            except IndexError as err:
                logger.warn('Object with UID %s not found in catalog: %s',
                             uid, err)
            else:
                if all_content_types or brain.portal_type.lower() in equivs:
                    try:
                        latest = brain.getObject()
                        versions = queryAdapter(latest, IGetVersions)
                        if versions is not None:
                            latest = versions.latest_version()
                        # on edit we don't want the context to be suggested
                        if latest != self.context:
                            url = '/' + latest.absolute_url(1)
                            if url not in candidates:
                                ob_to_candidate(
                                    latest, candidates, str(sim[1]))
                    except TypeError:
                        ob = brain.getObject()
                        if ob != self.context:
                            url = brain.getURL()
                            if url not in candidates:
                                ob_to_candidate(
                                    brain.getObject(), candidates, str(sim[1]))
            if len(candidates) == max_suggestions:
                break
        return json.dumps(candidates)


def ob_to_candidate(ob, candidates, similarity_score='unavailable'):
    """ Add object's details to the candidates dict """
    url = '/' + ob.absolute_url(1)
    creation_date = getSite().toLocalizedTime(ob.CreationDate())
    publish_date = getSite().toLocalizedTime(ob.EffectiveDate())
    candidates[url] = [ob.Title(), ob.Type(), creation_date,
                       publish_date or 'not available',
                       similarity_score]


def task_create_idf_index(context):
    """ create the idf index """
    site = getSite()
    catalog = site.portal_catalog
    settings = IEEASimilaritySettings(context).settings
    query = {}
    if catalog.Indexes.get('Language'):
        query['Language'] = 'en'

    texts = [[stem(word) for word in simple_preprocess(brain.Title,
              deacc=True) if not settings.remove_stopwords or
              word not in STOPWORDS] +
             [brain.UID.encode('utf8')]
             for brain in catalog(**query) if brain.Title]
    dictionary = corpora.Dictionary(texts)
    dictionary.save(SUGGESTIONS_PATH + '/dictionary.dict')
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize(SUGGESTIONS_PATH + '/corpus.mm', corpus)
    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=200)
    lsi.save(SUGGESTIONS_PATH + '/lsi.lsi')
    index = similarities.MatrixSimilarity(lsi[corpus], num_features=200)
    index.save(SUGGESTIONS_PATH + '/index.index')

    async_service = queryUtility(IAsyncService)
    if async_service is not None:
        frequency = settings.refresh_frequency or 24
        delay = datetime.timedelta(hours=frequency)
        queue = async_service.getQueues()['']
        async_service.queueJobInQueueWithDelay(
            None, datetime.datetime.now(pytz.UTC) + delay,
            queue, ('similarity',),
            task_create_idf_index,
            context
        )


class TFIDFIndex(BrowserView):
    """ creates dictionary, corpus, lsi and index for the TF-IDF"""

    def __call__(self):
        async_service = queryUtility(IAsyncService)
        if async_service is not None:
            queue = async_service.getQueues()['']
            async_service.queueJobInQueue(
                queue, ('similarity',),
                task_create_idf_index,
                self.context
            )
        else:
            task_create_idf_index(self.context)
        return "OK"


class SimilaritySettings(BrowserView):
    """ return parts of the registry settings
    """
    def enabled(self):
        """ return True if the similarity package is enabled """
        return IEEASimilaritySettings(self.context).enabled


class SuggestionsText(BrowserView):
    """ returns the title and the description of the suggestions dialog """

    def __call__(self):
        settings = IEEASimilaritySettings(self.context)
        text = [settings.dialog_title, settings.dialog_text,
                settings.dialog_title_no_suggestions,
                settings.dialog_text_no_suggestions]
        return json.dumps(text)
