""" Control Panel Interfaces

   >>> portal = layer['portal']
   >>> sandbox = portal['sandbox']

"""
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope.interface import Interface
from zope import schema
from plone.autoform import directives as aform
from eea.similarity.config import EEAMessageFactory as _
from decimal import Decimal


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

    threshold1 = schema.TextLine(
        title=_(u"Similarity threshold for 3-4 words titles"),
        description=_(
            u"Define the similarity score threshold for 3-4 words titles."
        ),
        required=True,
    )

    threshold2 = schema.TextLine(
        title=_(u"Similarity threshold for titles with more than 4 words"),
        description=_(
            u"Define the similarity score threshold for titles with "
            u"more than 4 words."
        ),
        required=True,
    )
