""" Control Panel Interfaces

   >>> portal = layer['portal']
   >>> sandbox = portal['sandbox']

"""
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope.interface import Interface
from zope import schema
from plone.autoform import directives as aform
from eea.similarity.config import EEAMessageFactory as _


class IEEASimilaritySettings(Interface):
    """ Settings

        >>> from eea.similarity.interfaces import IEEASimilaritySettings
        >>> IEEASimilaritySettings(portal).portalTypes
        [u'Document']

    """
    aform.widget('portalTypes', CheckBoxFieldWidget)
    portalTypes = schema.List(
        title=_(u"Enable similarity suggestions"),
        description=_(u"Suggestions for similar items are enabled for the "
                      u"following content-types"),
        required=False,
        default=[u"Document"],
        value_type=schema.Choice(
            vocabulary=u"plone.app.vocabularies.ReallyUserFriendlyTypes")
    )

    all_content_types = schema.Bool(
        title=_(u"Allow all content types"),
        description=_(
            u"Should all content types be taken into consideration when looking"
            u" for similar objects? (alternatively only the current object's "
            u" portal type and possible equivalent types are considered)."
        ),
        default=False,
        required=False,
    )

    min_words = schema.Int(
        title=_(u"Minimum number of words in title"),
        description=_(
            u"Suggestions are disabled for titles with less words"
        ),
        default=3,
        required=True,
    )

    equivalent_content_types = schema.List(
        title=_(u"Equivalent content types"),
        description=_(
            u"Please enter sets of equivalent content types, separated by"
            u" commas (each line a different set)"
        ),
        value_type=schema.TextLine(),
        required=False,
        default=[u'EEAFigure,DavizVisualization'],
    )

    number_of_suggestions = schema.Int(
        title=_(u"Max. number of suggestions"),
        description=_(
            u"Specify the maximum number of suggestions"
        ),
        default=3,
        required=True,
    )

    max_difference = schema.TextLine(
        title=_(u"Max. score difference between suggestions"),
        description=_(
            u"Specify the maximum similarity score difference between "
            u"displayed suggestions (set to 1 to disable):"
        ),
        default=u'0.2',
        required=True,
    )

    remove_stopwords = schema.Bool(
        title=_(u"Remove stopwords"),
        description=_(
            u"Should stopwords be removed from the titles before search?"
            u" (a change here will only have effects after an index rebuild)"
        ),
        default=True,
        required=False,
    )

    refresh_frequency = schema.Int(
        title=_(u"TF-IDF index refresh frequency"),
        description=_(
            u"Specify the interval (in hours) at which the TF-IDF index "
            u"should be rebuilt."
        ),
        default=24,
        required=False,
    )

    dialog_title = schema.TextLine(
        title=_(u"Dialog title"),
        description=_(
            u"Customise the title of the dialog window"
        ),
        default=u"Similar content found!",
        required=False,
    )

    dialog_text = schema.Text(
        title=_(u"Dialog text"),
        description=_(u"Customise the text of the dialog window"),
        default=(
            u"We have found very similar content based on the entered title "
            u"so far. They may be duplicates or possible content to link to."
        ),
        required=False,
    )

    dialog_title_no_suggestions = schema.TextLine(
        title=_(u"Dialog title - no suggestions"),
        description=_(
            u"Customise the title of the dialog window for the case when there"
            u" are no suggestions"
        ),
        default=u"Similar content",
        required=False,
    )

    dialog_text_no_suggestions = schema.Text(
        title=_(u"Dialog text - no suggestions"),
        description=_(
            u"Customise the text of the dialog window for the case when there"
            u" are no suggestions"
        ),
        default=u"There are no suggestions for duplicate content based on the"
                u" title",
        required=False,
    )

    threshold1 = schema.TextLine(
        title=_(u"Similarity threshold for titles with less than 5 words"),
        description=_(
            u"Define the similarity score threshold for titles"
            u" with less than 5 words."
        ),
        required=True,
        default=u'0.8',
    )

    threshold2 = schema.TextLine(
        title=_(u"Similarity threshold for titles with 5 or more words"),
        description=_(
            u"Define the similarity score threshold for titles with "
            u"more than 4 words."
        ),
        required=True,
        default=u'0.8',
    )
