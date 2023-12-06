"""
Courseware generalized definitions.
"""
from importlib import import_module

from django.conf import settings


def has_access(*args, **kwargs):
    """
    Wrapper for `lms.djangoapps.courseware.courses.has_access`
    """
    backend_function = settings.PLATFORM_PLUGIN_TEAMS_COURSEWARE_BACKEND
    backend = import_module(backend_function)

    return backend.has_access(*args, **kwargs)
