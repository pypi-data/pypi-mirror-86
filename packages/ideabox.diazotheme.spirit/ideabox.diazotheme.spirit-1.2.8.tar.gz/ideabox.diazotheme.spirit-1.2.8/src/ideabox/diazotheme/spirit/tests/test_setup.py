# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from ideabox.diazotheme.spirit.testing import IDEABOX_DIAZOTHEME_SPIRIT_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that ideabox.diazotheme.spirit is properly installed."""

    layer = IDEABOX_DIAZOTHEME_SPIRIT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if ideabox.diazotheme.spirit is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'ideabox.diazotheme.spirit'))

    def test_browserlayer(self):
        """Test that IIdeaboxDiazothemeSpiritLayer is registered."""
        from ideabox.diazotheme.spirit.interfaces import (
            IIdeaboxDiazothemeSpiritLayer)
        from plone.browserlayer import utils
        self.assertIn(IIdeaboxDiazothemeSpiritLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = IDEABOX_DIAZOTHEME_SPIRIT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(username=TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['ideabox.diazotheme.spirit'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if ideabox.diazotheme.spirit is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'ideabox.diazotheme.spirit'))

    def test_browserlayer_removed(self):
        """Test that IIdeaboxDiazothemeSpiritLayer is removed."""
        from ideabox.diazotheme.spirit.interfaces import \
            IIdeaboxDiazothemeSpiritLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IIdeaboxDiazothemeSpiritLayer,
            utils.registered_layers(),
        )
