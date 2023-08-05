# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFPlone.utils import get_installer
from library.theme.testing import LIBRARY_THEME_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that library.theme is properly installed."""

    layer = LIBRARY_THEME_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if library.theme is installed."""
        self.assertTrue(self.installer.isProductInstalled("library.theme"))

    def test_browserlayer(self):
        """Test that ILibraryThemeLayer is registered."""
        from library.theme.interfaces import ILibraryThemeLayer
        from plone.browserlayer import utils

        self.assertIn(ILibraryThemeLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = LIBRARY_THEME_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        roles_before = api.user.get_roles(username=TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstallProducts(["library.theme"])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if library.theme is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled("library.theme"))

    def test_browserlayer_removed(self):
        """Test that ILibraryThemeLayer is removed."""
        from library.theme.interfaces import ILibraryThemeLayer
        from plone.browserlayer import utils

        self.assertNotIn(ILibraryThemeLayer, utils.registered_layers())
