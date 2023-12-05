"""
Common settings for the plugin.
"""

INSTALLED_APPS = [
    "platform_plugin_teams",
]


def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.
    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.PLATFORM_PLUGIN_TEAMS_STUDENT_BACKEND = (
        "platform_plugin_teams.edxapp_wrapper.backends.student_p_v1"
    )
    settings.PLATFORM_PLUGIN_TEAMS_TEAMS_BACKEND = (
        "platform_plugin_teams.edxapp_wrapper.backends.teams_p_v1"
    )
    settings.PLATFORM_PLUGIN_TEAMS_COURSEWARE_BACKEND = (
        "platform_plugin_teams.edxapp_wrapper.backends.courseware_p_v1"
    )
    settings.PLATFORM_PLUGIN_TEAMS_MODULESTORE_BACKEND = (
        "platform_plugin_teams.edxapp_wrapper.backends.modulestore_p_v1"
    )
    settings.PLATFORM_PLUGIN_TEAMS_AUTHENTICATION_BACKEND = (
        "platform_plugin_teams.edxapp_wrapper.backends.authentication_p_v1"
    )
    settings.PLATFORM_PLUGIN_TEAMS_TEAMS_CONFIG_BACKEND = (
        "platform_plugin_teams.edxapp_wrapper.backends.teams_config_p_v1"
    )
    settings.PLATFORM_PLUGIN_TEAMS_CONTENTSTORE_BACKEND = (
        "platform_plugin_teams.edxapp_wrapper.backends.contentstore_p_v1"
    )
