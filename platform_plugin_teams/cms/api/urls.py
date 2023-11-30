"""URL patterns for the platform_plugin_teams plugin for the CMS."""
from django.urls import path

from platform_plugin_teams.cms.api import views

app_name = "platform_plugin_teams"

urlpatterns = [
    path("topics/", views.TopicsAPIView.as_view(), name="topics"),
    path("topics/<str:topic_id>/", views.TopicsAPIView.as_view(), name="delete-topics"),
]
