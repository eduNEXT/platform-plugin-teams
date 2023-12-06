"""
Student generalized definitions.
"""
from importlib import import_module

from django.conf import settings


def get_user_by_username_or_email(*args, **kwargs):
    """
    Wrapper for `student.models.user.get_user_by_username_or_email`
    """
    backend_function = settings.PLATFORM_PLUGIN_TEAMS_STUDENT_BACKEND
    backend = import_module(backend_function)

    return backend.get_user_by_username_or_email(*args, **kwargs)


def has_studio_write_access(*args, **kwargs):
    """
    Wrapper for `student.auth.has_studio_write_access`
    """
    backend_function = settings.PLATFORM_PLUGIN_TEAMS_STUDENT_BACKEND
    backend = import_module(backend_function)

    return backend.has_studio_write_access(*args, **kwargs)
