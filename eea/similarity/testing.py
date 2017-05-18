# -*- coding: utf-8 -*-
""" testing module
"""
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
import eea.similarity


class EeaSimilarityLayer(PloneSandboxLayer):
    """ EEA Similarity Layer """

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """ set up Zope"""
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=eea.similarity)

    def setUpPloneSite(self, portal):
        """ set up Plone site """
        applyProfile(portal, 'eea.similarity:default')

EEA_SIMILARITY_FIXTURE = EeaSimilarityLayer()

EEA_SIMILARITY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EEA_SIMILARITY_FIXTURE,),
    name='EeaSimilarityLayer:IntegrationTesting'
)

EEA_SIMILARITY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EEA_SIMILARITY_FIXTURE,),
    name='EeaSimilarityLayer:FunctionalTesting'
)

EEA_SIMILARITY_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        EEA_SIMILARITY_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='EeaSimilarityLayer:AcceptanceTesting'
)
