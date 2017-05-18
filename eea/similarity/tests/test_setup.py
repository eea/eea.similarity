# -*- coding: utf-8 -*-
""" Setup tests for this package.
"""
import unittest

from plone import api

from eea.similarity.testing import EEA_SIMILARITY_INTEGRATION_TESTING  # noqa


class TestSetup(unittest.TestCase):
    """Test that eea.similarity is properly installed."""

    layer = EEA_SIMILARITY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if eea.similarity is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'eea.similarity'))

    def test_browserlayer(self):
        """Test that IEeaSimilarityLayer is registered."""
        from eea.similarity.interfaces import (
            IEeaSimilarityLayer)
        from plone.browserlayer import utils
        self.assertIn(IEeaSimilarityLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):
    """Test that eea.similarity is properly uninstalled."""

    layer = EEA_SIMILARITY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['eea.similarity'])

    def test_product_uninstalled(self):
        """Test if eea.similarity is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'eea.similarity'))

    def test_browserlayer_removed(self):
        """Test that IEeaSimilarityLayer is removed."""
        from eea.similarity.interfaces import \
            IEeaSimilarityLayer
        from plone.browserlayer import utils
        self.assertNotIn(IEeaSimilarityLayer, utils.registered_layers())
