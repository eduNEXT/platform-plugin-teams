"""
Teams common generalized definitions.
"""
from importlib import import_module

from django.conf import settings


def get_course_team_model():
    """
    Wrapper for `teams.models.CourseTeam`
    """
    backend_function = settings.PLATFORM_PLUGIN_TEAMS_TEAMS_COMMON_BACKEND
    backend = import_module(backend_function)

    return backend.CourseTeam


CourseTeam = get_course_team_model()
