""" This file contains the API views for the Teams plugin. """ ""
from copy import deepcopy
from uuid import uuid4

from common.djangoapps.student.auth import has_studio_write_access
from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from edx_rest_framework_extensions.auth.session.authentication import SessionAuthenticationAllowInactiveUser
from lms.djangoapps.teams.models import CourseTeam
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey
from openedx.core.lib.api.authentication import BearerAuthenticationAllowInactiveUser
from openedx.core.lib.teams_config import TeamsetType
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from xmodule.modulestore.django import modulestore

from platform_plugin_teams.utils import api_field_errors


class TopicsAPIView(GenericAPIView):
    """
    API view for the topics endpoints.

    This class provides POST and DELETE methods for interacting with topics related to a course.

    `Use Cases`:

        * POST: Add a new topic to a course.
        * DELETE: Delete a topic from a course. This will also delete all teams
            associated with the topic, and remove all members from those teams.

    `Example Requests`:

        * POST: /platform-plugin-teams/{course-id}/api/cms/topics/

            * Path Parameters:
                * course_id (str): The course id for the course to add a topic to (required).

            * Body Parameters:
                * name (str): The name of the topic to add (required).
                * description (str): The description of the topic to add (required).
                * type (str): The type of the topic to add (required).
                * max_team_size (int): The max team size of the topic to add (required).

        * DELETE: /platform-plugin-teams/{course-id}/api/cms/topics/{topic-id}/

            * Path Parameters:
                * course_id (str): The course id for the course to delete a topic from (required).
                * topic_id (str): The topic id for the topic to delete (required).

    `Example Responses`:

        * POST: /platform-plugin-teams/{course-id}/api/cms/topics/

            * 400:
                * The topic name already exists for the course.

            * 404:
                * The supplied course_id does not exists.
                * The supplied course is not found.

            * 201: Returns a list of updated topics for the course.

                The response body will contain the following fields:

                * topics: A list of updated topics for the course.

                    * id (str): The topic's unique identifier.
                    * name (str): The name of the topic.
                    * description (str): A description of the topic.
                    * type (str): The type of the topic.
                    * max_team_size (int): The max team size of the topic.

        * DELETE: /platform-plugin-teams/{course-id}/api/cms/topics/{topic-id}/

            * 404:
                * The supplied course_id does not exists.
                * The supplied course is not found.
                * The supplied topic_id does not exists.

            * 204: Returns a list of updated topics for the course.

                The response body will contain the following fields:

                * topics (list): A list of updated topics for the course.

                    * id (str): The topic's unique identifier.
                    * name (str): The name of the topic.
                    * description (str): A description of the topic.
                    * type (str): The type of the topic.
                    * max_team_size (int): The max team size of the topic.
    """

    authentication_classes = (
        JwtAuthentication,
        BearerAuthenticationAllowInactiveUser,
        SessionAuthenticationAllowInactiveUser,
    )
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, course_id: str):
        """POST request handler for the topics view."""
        from cms.djangoapps.contentstore.views.course import update_course_advanced_settings

        new_topic = deepcopy(request.data)

        valid_team_types = [team_type.value for team_type in TeamsetType]
        if new_topic.get("type") not in valid_team_types:
            return api_field_errors(
                {"type": f"The [type] field must be one of {valid_team_types}."},
            )

        try:
            course_key = CourseKey.from_string(course_id)
        except InvalidKeyError:
            return api_field_errors(
                {"course_id": f"The supplied {course_id=} does not exists."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        course_block = modulestore().get_course(course_key)
        if course_block is None:
            return api_field_errors(
                {"course_id": f"The supplied {course_id=} is not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if not has_studio_write_access(request.user, course_key):
            self.permission_denied(request)

        teams_configuration = deepcopy(course_block.teams_configuration.cleaned_data)

        for topic in teams_configuration["team_sets"]:
            if topic["name"].lower() == (name := request.data.get("name").lower()):
                return api_field_errors(
                    {"name": f"The topic with {name=} already exists."}
                )

        new_topic["id"] = str(uuid4())
        teams_configuration["team_sets"].append(new_topic)
        data = {"teams_configuration": {"value": teams_configuration}}
        updated_data = update_course_advanced_settings(course_block, data, request.user)

        return Response(
            {"topics": updated_data["teams_configuration"]["value"]["team_sets"]},
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, course_id: str, topic_id: str):
        """DELETE request handler for the topics view."""
        from cms.djangoapps.contentstore.views.course import update_course_advanced_settings

        try:
            course_key = CourseKey.from_string(course_id)
        except InvalidKeyError:
            return api_field_errors(
                {"course_id": f"The supplied {course_id=} does not exists."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        course_block = modulestore().get_course(course_key)
        if course_block is None:
            return api_field_errors(
                {"course_id": f"The supplied {course_id=} is not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if not has_studio_write_access(request.user, course_key):
            self.permission_denied(request)

        teams_configuration = deepcopy(course_block.teams_configuration.cleaned_data)

        topic_exists = False
        for topic in teams_configuration["team_sets"]:
            if topic["id"] == topic_id:
                teams_configuration["team_sets"].remove(topic)
                topic_exists = True
                break

        if not topic_exists:
            return api_field_errors(
                {"topic_id": f"The supplied {topic_id=} is not found."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        data = {"teams_configuration": {"value": teams_configuration}}
        updated_data = update_course_advanced_settings(course_block, data, request.user)

        teams = CourseTeam.objects.filter(topic_id=topic_id)
        for team in teams:
            team.membership.all().delete()
            team.delete()

        return Response(
            {"topics": updated_data["teams_configuration"]["value"]["team_sets"]},
            status=status.HTTP_204_NO_CONTENT,
        )
