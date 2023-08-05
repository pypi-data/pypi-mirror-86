# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import library.theme


class LibraryThemeLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=library.theme)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'library.theme:default')


LIBRARY_THEME_FIXTURE = LibraryThemeLayer()


LIBRARY_THEME_INTEGRATION_TESTING = IntegrationTesting(
    bases=(LIBRARY_THEME_FIXTURE,),
    name='LibraryThemeLayer:IntegrationTesting'
)


LIBRARY_THEME_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(LIBRARY_THEME_FIXTURE,),
    name='LibraryThemeLayer:FunctionalTesting'
)


LIBRARY_THEME_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        LIBRARY_THEME_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='LibraryThemeLayer:AcceptanceTesting'
)
