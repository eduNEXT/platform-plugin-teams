"""
Teams Config generalized definitions.
"""
from importlib import import_module

from django.conf import settings


def get_teamset_type_enum():
    """
    Wrapper for `openedx.core.lib.teams_config.TeamsetType`
    """
    backend_function = settings.PLATFORM_PLUGIN_TEAMS_TEAMS_CONFIG_BACKEND
    backend = import_module(backend_function)

    return backend.TeamsetType


TeamsetType = get_teamset_type_enum()
