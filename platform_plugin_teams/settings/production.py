"""
Production settings for the plugin.
"""


def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.
    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.PLATFORM_PLUGIN_TEAMS_STUDENT_BACKEND = getattr(
        settings, "ENV_TOKENS", {}
    ).get(
        "PLATFORM_PLUGIN_TEAMS_STUDENT_BACKEND",
        settings.PLATFORM_PLUGIN_TEAMS_STUDENT_BACKEND,
    )
    settings.PLATFORM_PLUGIN_TEAMS_TEAMS_BACKEND = getattr(
        settings, "ENV_TOKENS", {}
    ).get(
        "PLATFORM_PLUGIN_TEAMS_TEAMS_BACKEND",
        settings.PLATFORM_PLUGIN_TEAMS_TEAMS_BACKEND,
    )
    settings.PLATFORM_PLUGIN_TEAMS_COURSEWARE_BACKEND = getattr(
        settings, "ENV_TOKENS", {}
    ).get(
        "PLATFORM_PLUGIN_TEAMS_COURSEWARE_BACKEND",
        settings.PLATFORM_PLUGIN_TEAMS_COURSEWARE_BACKEND,
    )
    settings.PLATFORM_PLUGIN_TEAMS_MODULESTORE_BACKEND = getattr(
        settings, "ENV_TOKENS", {}
    ).get(
        "PLATFORM_PLUGIN_TEAMS_MODULESTORE_BACKEND",
        settings.PLATFORM_PLUGIN_TEAMS_MODULESTORE_BACKEND,
    )
    settings.PLATFORM_PLUGIN_TEAMS_AUTHENTICATION_BACKEND = getattr(
        settings, "ENV_TOKENS", {}
    ).get(
        "PLATFORM_PLUGIN_TEAMS_AUTHENTICATION_BACKEND",
        settings.PLATFORM_PLUGIN_TEAMS_AUTHENTICATION_BACKEND,
    )
    settings.PLATFORM_PLUGIN_TEAMS_TEAMS_CONFIG_BACKEND = getattr(
        settings, "ENV_TOKENS", {}
    ).get(
        "PLATFORM_PLUGIN_TEAMS_TEAMS_CONFIG_BACKEND",
        settings.PLATFORM_PLUGIN_TEAMS_TEAMS_CONFIG_BACKEND,
    )
    settings.PLATFORM_PLUGIN_TEAMS_CONTENTSTORE_BACKEND = getattr(
        settings, "ENV_TOKENS", {}
    ).get(
        "PLATFORM_PLUGIN_TEAMS_CONTENTSTORE_BACKEND",
        settings.PLATFORM_PLUGIN_TEAMS_CONTENTSTORE_BACKEND,
    )
