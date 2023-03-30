"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFPlone.utils import get_installer
from rfaqsl.testing import RFAQSL_INTEGRATION_TESTING  # noqa: E501

import unittest


class TestSetup(unittest.TestCase):
    """Test that rfaqsl is properly installed."""

    layer = RFAQSL_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.setup = self.portal.portal_setup
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if rfaqsl is installed."""
        self.assertTrue(self.installer.is_product_installed("rfaqsl"))

    def test_browserlayer(self):
        """Test that IRFAQSLLayer is registered."""
        from plone.browserlayer import utils
        from rfaqsl.interfaces import IRFAQSLLayer

        self.assertIn(IRFAQSLLayer, utils.registered_layers())

    def test_latest_version(self):
        """Test latest version of default profile."""
        self.assertEqual(
            self.setup.getLastVersionForProfile("rfaqsl:default")[0],
            "20221205001",
        )


class TestUninstall(unittest.TestCase):

    layer = RFAQSL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("rfaqsl")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if rfaqsl is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("rfaqsl"))

    def test_browserlayer_removed(self):
        """Test that IRFAQSLLayer is removed."""
        from plone.browserlayer import utils
        from rfaqsl.interfaces import IRFAQSLLayer

        self.assertNotIn(IRFAQSLLayer, utils.registered_layers())
