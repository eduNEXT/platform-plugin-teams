"""
platform_plugin_teams Django application initialization.
"""

from django.apps import AppConfig

from openedx.core.constants import COURSE_ID_PATTERN


class PlatformPluginTeamsConfig(AppConfig):
    """
    Configuration for the platform_plugin_teams Django application.
    """

    name = "platform_plugin_teams"
    verbose_name = "Custom Teams API Plugin"

    plugin_app = {
        "url_config": {
            "lms.djangoapp": {
                "namespace": "platform-plugin-teams",
                "regex": rf"platform-plugin-teams/{COURSE_ID_PATTERN}/",
                "relative_path": "urls",
            },
            "cms.djangoapp": {
                "namespace": "platform-plugin-teams",
                "regex": rf"platform-plugin-teams/{COURSE_ID_PATTERN}/",
                "relative_path": "urls",
            },
        },
        "settings_config": {
            "lms.djangoapp": {
                "test": {"relative_path": "settings.test"},
                "common": {"relative_path": "settings.common"},
                "production": {"relative_path": "settings.production"},
            },
        },
    }
