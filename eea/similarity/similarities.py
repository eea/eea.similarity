import os
import json
import logging
from Products.Five import BrowserView
from zope.component.hooks import getSite
from gensim import corpora, models, similarities
from collections import defaultdict
from stemming.porter2 import stem
from eea.similarity.interfaces import IEEASimilaritySettings
try:
    from eea.versions.interfaces import IGetVersions
except ImportError:
    pass

MAX_DIFFERENCE = 0.1
SUGGESTIONS_PATH = os.environ.get('EEASUGGESTIONS_PATH', '/tmp')
EQUIV_TYPES = {
    'EEAFigure': ['EEAFigure', 'DavizVisualization'],
    'DavizVisualization': ['EEAFigure', 'DavizVisualization'],
}

logger = logging.getLogger('eea.similarity')


def get_gensim_data():
    dictionary = corpora.Dictionary.load(SUGGESTIONS_PATH +
                                         '/dictionary.dict')
    corpus = corpora.MmCorpus(SUGGESTIONS_PATH +  '/corpus.mm')
    lsi = models.LsiModel.load(SUGGESTIONS_PATH +  '/lsi.lsi')
    index = similarities.MatrixSimilarity.load(SUGGESTIONS_PATH +
                                               '/index.index')
    return dictionary, corpus, lsi, index

class Suggestions(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request


    def reference_threshold(self, length):
        similarity_settings = IEEASimilaritySettings(self.context).settings
        if length > 4:
            return float(similarity_settings.threshold2)
        elif length > 2:
            return float(similarity_settings.threshold1)


    def __call__(self):
        '''returns a json with candidates of duplication'''
        if self.context.getLanguage() != 'en':
            #suggestions only work for English
            return
        catalog = getSite().portal_catalog
        candidates = {}
        title = self.request.get('title')
        words = title.lower().split()
        portal_type = self.request.get('portal_type')
        if len(words) < 3:
            brains = catalog({'Title': words})[:3]
            for brain in brains:
                if brain.portal_type == portal_type:
                    candidates[brain.getURL()] = [brain.Title, 'unavailable']
        else:
            dictionary, corpus, lsi, index = get_gensim_data()
            vec_bow = dictionary.doc2bow([stem(word) for word in words])
            vec_lsi = lsi[vec_bow]
            sims = index[vec_lsi]
            sims = sorted(enumerate(sims), key=lambda item: -item[1])
            previous_note = 0
            for sim in sims:
                if sim[1] < self.reference_threshold(
                        len(title.lower().split())) or (
                        previous_note - sim[1] > MAX_DIFFERENCE):
                    # if the difference in similarity is big, next candidates are
                    # no longer interesting
                    break
                previous_note = sim[1]

                for word_id in corpus[sim[0]]:
                    if len(dictionary[word_id[0]].replace('-', '')) == 32:
                        uid = dictionary[word_id[0]]
                        break
                try:
                    brain = catalog({'UID': [uid, uid.upper()]})[0]
                except NameError:
                    logger.error('Catalog UID not found')
                except IndexError:
                    logger.error('Object with UID %s not found in catalog' % uid)
                else:
                    if brain.portal_type in EQUIV_TYPES.get(
                            portal_type, [portal_type]):
                        try:
                            versions = IGetVersions(brain.getObject())
                            latest = versions.latest_version()
                            url = '/' + latest.absolute_url(1)
                            if url not in candidates:
                                candidates[url] = [latest.title, str(sim[1])]
                        except TypeError:
                            url = brain.getURL()
                            if url not in candidates:
                                candidates[url] = [
                                    brain.Title, str(sim[1])]
                if len(candidates) == 5:
                    break
        return json.dumps(candidates)



class TFIDFIndex(BrowserView):
    """ creates dictionary, corpus, lsi and index for the TF-IDF"""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        site = getSite()
        catalog = site.portal_catalog
        texts = [[stem(word) for word in brain.Title.lower().split()] +
                  [brain.UID.encode('utf8')]
                  for brain in catalog(Language='en') if brain.Title]
        dictionary = corpora.Dictionary(texts)
        dictionary.save(SUGGESTIONS_PATH +  '/dictionary.dict')
        corpus = [dictionary.doc2bow(text) for text in texts]
        corpora.MmCorpus.serialize(SUGGESTIONS_PATH +  '/corpus.mm', corpus)
        lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=200)
        lsi.save(SUGGESTIONS_PATH +  '/lsi.lsi')
        index = similarities.MatrixSimilarity(lsi[corpus], num_features=200)
        index.save(SUGGESTIONS_PATH +  '/index.index')


class SimilaritySettings(BrowserView):
    """ return parts of the registry settings """

    def enabled(self):
        return IEEASimilaritySettings(self.context).enabled
