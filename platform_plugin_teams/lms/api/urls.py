"""URL patterns for the platform_plugin_teams API in the LMS."""
from django.urls import path

from platform_plugin_teams.lms.api import views

app_name = "platform_plugin_teams"

urlpatterns = [
    path("topics/", views.TopicsReadOnlyAPIView.as_view(), name="topics-read-only-api"),
    path(
        "team-membership/",
        views.TeamMembershipAPIView.as_view(),
        name="team-membership-api",
    ),
]
