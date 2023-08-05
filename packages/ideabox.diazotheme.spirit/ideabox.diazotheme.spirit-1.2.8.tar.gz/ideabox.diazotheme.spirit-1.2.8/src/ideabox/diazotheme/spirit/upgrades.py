# -*- coding: utf-8 -*-

from plone import api


def reload_registry(context):
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(
        "profile-ideabox.diazotheme.spirit:default", "plone.app.registry"
    )


def to_1001(context):
    """ Add a portal action for informations """
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(
        "profile-ideabox.diazotheme.spirit:default", "actions"
    )
