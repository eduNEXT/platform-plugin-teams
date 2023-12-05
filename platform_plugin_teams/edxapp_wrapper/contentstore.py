"""
Contentstore generalized definitions.
"""
from importlib import import_module

from django.conf import settings


def update_course_advanced_settings(*args, **kwargs):
    """
    Wrapper for `cms.djangoapps.contentstore.views.course.update_course_advanced_settings`
    """
    backend_function = settings.PLATFORM_PLUGIN_TEAMS_CONTENTSTORE_BACKEND
    backend = import_module(backend_function)

    return backend.update_course_advanced_settings(*args, **kwargs)
