# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import collective.debug


class CollectiveDebugLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.debug)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.debug:default')


COLLECTIVE_DEBUG_FIXTURE = CollectiveDebugLayer()


COLLECTIVE_DEBUG_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_DEBUG_FIXTURE,),
    name='CollectiveDebugLayer:IntegrationTesting',
)


COLLECTIVE_DEBUG_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_DEBUG_FIXTURE,),
    name='CollectiveDebugLayer:FunctionalTesting',
)


COLLECTIVE_DEBUG_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_DEBUG_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectiveDebugLayer:AcceptanceTesting',
)
