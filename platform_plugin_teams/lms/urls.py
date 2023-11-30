"""URL patterns for the platform_plugin_teams plugin for the LMS."""
from django.urls import include, path

app_name = "platform_plugin_teams"

urlpatterns = [
    path(
        "api/",
        include(
            "platform_plugin_teams.lms.api.urls",
            namespace="platform-plugin-teams-lms-api",
        ),
    ),
]
