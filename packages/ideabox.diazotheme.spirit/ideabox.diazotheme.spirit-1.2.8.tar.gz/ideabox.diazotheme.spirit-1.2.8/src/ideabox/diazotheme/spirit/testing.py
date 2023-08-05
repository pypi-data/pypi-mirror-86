# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import ideabox.diazotheme.spirit


class IdeaboxDiazothemeSpiritLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=ideabox.diazotheme.spirit)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ideabox.diazotheme.spirit:default')


IDEABOX_DIAZOTHEME_SPIRIT_FIXTURE = IdeaboxDiazothemeSpiritLayer()


IDEABOX_DIAZOTHEME_SPIRIT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(IDEABOX_DIAZOTHEME_SPIRIT_FIXTURE,),
    name='IdeaboxDiazothemeSpiritLayer:IntegrationTesting'
)


IDEABOX_DIAZOTHEME_SPIRIT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(IDEABOX_DIAZOTHEME_SPIRIT_FIXTURE,),
    name='IdeaboxDiazothemeSpiritLayer:FunctionalTesting'
)


IDEABOX_DIAZOTHEME_SPIRIT_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        IDEABOX_DIAZOTHEME_SPIRIT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='IdeaboxDiazothemeSpiritLayer:AcceptanceTesting'
)
