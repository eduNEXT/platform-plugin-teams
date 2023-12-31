"""
Teams LMS generalized definitions.
"""
from importlib import import_module

from django.conf import settings


def can_user_modify_team(*args, **kwargs):
    """
    Wrapper for `teams.api.can_user_modify_team`
    """
    backend_function = settings.PLATFORM_PLUGIN_TEAMS_TEAMS_LMS_BACKEND
    backend = import_module(backend_function)

    return backend.can_user_modify_team(*args, **kwargs)


def get_team_by_team_id(*args, **kwargs):
    """
    Wrapper for `teams.api.get_team_by_team_id`
    """
    backend_function = settings.PLATFORM_PLUGIN_TEAMS_TEAMS_LMS_BACKEND
    backend = import_module(backend_function)

    return backend.get_team_by_team_id(*args, **kwargs)


def has_specific_team_access(*args, **kwargs):
    """
    Wrapper for `teams.api.has_specific_team_access`
    """
    backend_function = settings.PLATFORM_PLUGIN_TEAMS_TEAMS_LMS_BACKEND
    backend = import_module(backend_function)

    return backend.has_specific_team_access(*args, **kwargs)


def has_team_api_access(*args, **kwargs):
    """
    Wrapper for `teams.api.has_team_api_access`
    """
    backend_function = settings.PLATFORM_PLUGIN_TEAMS_TEAMS_LMS_BACKEND
    backend = import_module(backend_function)

    return backend.has_team_api_access(*args, **kwargs)


def user_organization_protection_status(*args, **kwargs):
    """
    Wrapper for `teams.api.user_organization_protection_status`
    """
    backend_function = settings.PLATFORM_PLUGIN_TEAMS_TEAMS_LMS_BACKEND
    backend = import_module(backend_function)

    return backend.user_organization_protection_status(*args, **kwargs)


def get_already_on_team_in_teamset_error():
    """
    Wrapper for `teams.errors.AlreadyOnTeamInTeamset`
    """
    backend_function = settings.PLATFORM_PLUGIN_TEAMS_TEAMS_LMS_BACKEND
    backend = import_module(backend_function)

    return backend.AlreadyOnTeamInTeamset


def get_not_enrolled_in_course_for_team_error():
    """
    Wrapper for `teams.errors.NotEnrolledInCourseForTeam`
    """
    backend_function = settings.PLATFORM_PLUGIN_TEAMS_TEAMS_LMS_BACKEND
    backend = import_module(backend_function)

    return backend.NotEnrolledInCourseForTeam


def get_course_team_membership_model():
    """
    Wrapper for `teams.models.CourseTeamMembership`
    """
    backend_function = settings.PLATFORM_PLUGIN_TEAMS_TEAMS_LMS_BACKEND
    backend = import_module(backend_function)

    return backend.CourseTeamMembership


def get_membership_serializer():
    """
    Wrapper for `teams.serializers.MembershipSerializer`
    """
    backend_function = settings.PLATFORM_PLUGIN_TEAMS_TEAMS_LMS_BACKEND
    backend = import_module(backend_function)

    return backend.MembershipSerializer


def get_bulk_team_count_topic_serializer():
    """
    Wrapper for `teams.serializers.BulkTeamCountTopicSerializer`
    """
    backend_function = settings.PLATFORM_PLUGIN_TEAMS_TEAMS_LMS_BACKEND
    backend = import_module(backend_function)

    return backend.BulkTeamCountTopicSerializer


def get_course_team_serializer():
    """
    Wrapper for `teams.serializers.CourseTeamSerializer`
    """
    backend_function = settings.PLATFORM_PLUGIN_TEAMS_TEAMS_LMS_BACKEND
    backend = import_module(backend_function)

    return backend.CourseTeamSerializer


def get_topics_pagination_view():
    """
    Wrapper for `teams.views.TopicsPagination`
    """
    backend_function = settings.PLATFORM_PLUGIN_TEAMS_TEAMS_LMS_BACKEND
    backend = import_module(backend_function)

    return backend.TopicsPagination


def _filter_hidden_private_teamsets(*args, **kwargs):
    """
    Wrapper for `teams.views._filter_hidden_private_teamsets`
    """
    backend_function = settings.PLATFORM_PLUGIN_TEAMS_TEAMS_LMS_BACKEND
    backend = import_module(backend_function)

    return backend._filter_hidden_private_teamsets(  # pylint: disable=protected-access
        *args, **kwargs
    )


def get_alphabetical_topics(*args, **kwargs):
    """
    Wrapper for `teams.views.get_alphabetical_topics`
    """
    backend_function = settings.PLATFORM_PLUGIN_TEAMS_TEAMS_LMS_BACKEND
    backend = import_module(backend_function)

    return backend.get_alphabetical_topics(*args, **kwargs)


AlreadyOnTeamInTeamset = get_already_on_team_in_teamset_error()
NotEnrolledInCourseForTeam = get_not_enrolled_in_course_for_team_error()
CourseTeamMembership = get_course_team_membership_model()
MembershipSerializer = get_membership_serializer()
TopicsPagination = get_topics_pagination_view()
BulkTeamCountTopicSerializer = get_bulk_team_count_topic_serializer()
CourseTeamSerializer = get_course_team_serializer()
