"""
platform_plugin_teams Django application initialization.
"""

from django.apps import AppConfig


class PlatformPluginTeamsConfig(AppConfig):
    """
    Configuration for the platform_plugin_teams Django application.
    """

    name = "platform_plugin_teams"
    verbose_name = "Custom Teams API Plugin"

    plugin_app = {
        "url_config": {
            "lms.djangoapp": {
                "namespace": "custom-teams",
                "regex": r"^custom-teams/",
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
