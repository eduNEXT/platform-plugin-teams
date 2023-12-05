"""URL patterns for the platform_plugin_teams plugin."""
from django.conf import settings
from django.urls import include, path

app_name = "platform_plugin_teams"

if settings.SERVICE_VARIANT == "lms":
    urlpatterns = [
        path(
            "",
            include(
                "platform_plugin_teams.api.lms.urls",
                namespace="platform-plugin-teams-lms-api",
            ),
        ),
    ]
elif settings.SERVICE_VARIANT == "cms":
    urlpatterns = [
        path(
            "",
            include(
                "platform_plugin_teams.api.cms.urls",
                namespace="platform-plugin-teams-cms-api",
            ),
        ),
    ]
