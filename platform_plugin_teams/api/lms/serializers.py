"""Serializers for the Teams API."""
from lms.djangoapps.teams.models import CourseTeam
from lms.djangoapps.teams.serializers import BulkTeamCountTopicSerializer, CourseTeamSerializer
from rest_framework import serializers


class CustomTeamSerializer(BulkTeamCountTopicSerializer):
    """
    Serializer for add teams information to the topic.

    This is a subclass of the BulkTeamCountTopicSerializer. The purpose of this
    subclass is add the `teams` field, which is a list of teams.
    """

    teams = serializers.SerializerMethodField()

    def get_teams(self, topic: dict) -> list:
        """
        Get the teams for a given topic.

        Args:
            topic (dict): The topic for which to get the teams.

        Returns:
            list: A list of teams for the given topic.
        """
        result_filter = self.context["result_filter"]
        excluded_private_team_ids = self.context["excluded_private_team_ids"]

        result_filter.update({"topic_id": topic.get("id")})
        queryset = CourseTeam.objects.filter(**result_filter).exclude(
            team_id__in=excluded_private_team_ids
        )
        team_serializer = CourseTeamSerializer(
            queryset, context={"request": self.context["request"]}, many=True
        )

        return team_serializer.data
