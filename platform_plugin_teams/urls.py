"""URL patterns for the platform_plugin_teams plugin."""
from django.urls import include, path

app_name = "platform_plugin_teams"

urlpatterns = [
    path(
        "api/",
        include(
            "platform_plugin_teams.api.urls",
            namespace="platform-plugin-teams-api",
        ),
    ),
]
