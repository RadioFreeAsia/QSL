from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing.zope import WSGI_SERVER_FIXTURE

import rfaqsl


class RFAQSLLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=rfaqsl)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "rfaqsl:default")
        applyProfile(portal, "rfaqsl:initial")


RFAQSL_FIXTURE = RFAQSLLayer()


RFAQSL_INTEGRATION_TESTING = IntegrationTesting(
    bases=(RFAQSL_FIXTURE,),
    name="RFAQSLLayer:IntegrationTesting",
)


RFAQSL_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(RFAQSL_FIXTURE, WSGI_SERVER_FIXTURE),
    name="RFAQSLLayer:FunctionalTesting",
)


RFAQSLACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        RFAQSL_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        WSGI_SERVER_FIXTURE,
    ),
    name="RFAQSLLayer:AcceptanceTesting",
)
