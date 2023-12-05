"""API views for the teams plugin in the LMS"""
from django.contrib.auth import get_user_model
from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from edx_rest_framework_extensions.auth.session.authentication import SessionAuthenticationAllowInactiveUser
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from platform_plugin_teams.api.lms.serializers import CustomTeamSerializer
from platform_plugin_teams.edxapp_wrapper.authentication import BearerAuthenticationAllowInactiveUser
from platform_plugin_teams.edxapp_wrapper.courseware import has_access
from platform_plugin_teams.edxapp_wrapper.modulestore import modulestore
from platform_plugin_teams.edxapp_wrapper.student import get_user_by_username_or_email
from platform_plugin_teams.edxapp_wrapper.teams_common import CourseTeam
from platform_plugin_teams.edxapp_wrapper.teams_lms import (
    AlreadyOnTeamInTeamset,
    CourseTeamMembership,
    MembershipSerializer,
    NotEnrolledInCourseForTeam,
    TopicsPagination,
    _filter_hidden_private_teamsets,
    can_user_modify_team,
    get_alphabetical_topics,
    get_team_by_team_id,
    has_specific_team_access,
    has_team_api_access,
    user_organization_protection_status,
)
from platform_plugin_teams.utils import api_error, api_field_errors

User = get_user_model()


class TopicsReadOnlyAPIView(GenericAPIView):
    """
    API view for the topics endpoints.

    This class provides GET method for interacting with topics related to a course.

    `Use Cases`:

        * GET: Get a list of topics for a course.

    `Example Requests`:

        * GET: /platform-plugin-teams/{course_id}/api/topics/?page={page}&page_size={page_size}

            * Path Parameters:
                * course_id (str): The course id for the course to get topics for (required).

            * Query Parameters:
                * page (int): The page number to return (optional).
                * page_size (int): The number of results to return per page (optional).

    `Example Responses`:

        * GET: /platform-plugin-teams/{course_id}/api/topics/?page={page}&page_size={page_size}

            * 404:
                * The supplied course_id does not exists.
                * The supplied course is not found.

            * 403:
                * The user do not have access to the Team API for the given course.

            * 200: Returns a list of topics for the given course.

                The response body will contain the following fields:

                * count (int): The total number of topics matching the request.
                * next (str): The URL to the next page of results, or null if this is the
                    last page.
                * previous (str): The URL to the previous page of results, or null if this
                    is the first page.
                * num_pages (int): The total number of pages in the result.
                * start (int): The index of the first result in the current page.
                * current_page (int): The current page number.

                * results (list): A list of the topics matching the request.

                    * id (str): The topic's unique identifier.
                    * name (str): The name of the topic.
                    * description (str): A description of the topic.
                    * type (str): The type of the topic.
                    * max_team_size (int): The max team size of the topic.
                    * team_count (int): Number of teams created under the topic.
                    * teams (list[dict]): A list of teams under the topic.
    """

    authentication_classes = (
        JwtAuthentication,
        BearerAuthenticationAllowInactiveUser,
        SessionAuthenticationAllowInactiveUser,
    )
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = TopicsPagination
    queryset = []

    def get(self, request, course_id: str):
        """GET request handler for the topics view."""
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

        if not has_team_api_access(request.user, course_key):
            return api_error(
                f"The {request.user=} do not have access to the Team API for the given course.",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        organization_protection_status = user_organization_protection_status(
            request.user, course_key
        )
        topics = get_alphabetical_topics(course_block)
        topics = _filter_hidden_private_teamsets(request.user, topics, course_block)

        result_filter = {}
        organization_protection_status = user_organization_protection_status(
            request.user, course_key
        )
        if not organization_protection_status.is_exempt:
            result_filter.update(
                {"organization_protected": organization_protection_status.is_protected}
            )

        # Hide private_managed courses from non-staff users that aren't members of those teams
        excluded_private_team_ids = self._get_private_team_ids_to_exclude(course_block)
        context = {
            "request": request,
            "course_id": course_key,
            "organization_protection_status": organization_protection_status,
            "excluded_private_team_ids": excluded_private_team_ids,
            "result_filter": result_filter,
        }

        # Use the serializer that adds team info per topic
        serializer = CustomTeamSerializer(
            self.paginate_queryset(topics),
            context=context,
            many=True,
        )

        response = self.get_paginated_response(serializer.data)

        return response

    def _get_private_team_ids_to_exclude(self, course_block):
        """
        Get the list of team ids that should be excluded from the response.

        Users should not be able to see teams in private teamsets they are not members
        of unless they're staff.
        """
        if has_access(self.request.user, "staff", course_block.id):
            return set()

        private_teamset_ids = [
            teamset.teamset_id
            for teamset in course_block.teamsets
            if teamset.is_private_managed
        ]
        excluded_team_ids = (
            CourseTeam
            .objects.filter(course_id=course_block.id, topic_id__in=private_teamset_ids)
            .exclude(membership__user=self.request.user)
            .values_list("team_id", flat=True)
        )
        return set(excluded_team_ids)


class TeamMembershipAPIView(GenericAPIView):
    """
    API view for the team membership endpoints.

    This class provides POST method for interacting with team membership related to a course.

    `Use Cases`:

        * POST: Add a list of users to a team. If the user is already on a team,
            they will be removed from that team and added to the new team.

    `Example Requests`:

        * POST: /platform-plugin-teams/{course_id}/api/team-membership/

            * Body Parameters:
                * usernames (list): The usernames of the users to add to the team (required).
                * team_id (str): The team id for the team to add the user to (required).

    `Example Responses`:

        * POST: /platform-plugin-teams/{course_id}/api/team-membership/

            * 400:
                * The usernames and/or team_id is missing from the request body.
                * The team does not have enough space for the given users.
                * The user is not enrolled in the course associated with this team.

            * 404:
                * The supplied team_id does not exists.
                * The supplied username does not exists.

            * 403:
                * The user do not have access to the Team API for the given course.
                * The user do not have access to the specified team.
                * The user can not join an instructor managed team.

            * 201: The users were added to the team.

                The response body will contain the following fields:

                * memberships (list[dict]): A list of the memberships that were created.

                    * user (dict): The user that was added to the team.
                        * url: The url to the user profile.
                        * username: The username of the user.

                    * team (dict): The team that the user was added to.
                        * url: The url to the team.
                        * team_id: The team id of the team.

                    * date_joined (str): The date the user was added to the team.
                    * last_activity_at (str): The date the user was last active on the team.
    """

    authentication_classes = (
        JwtAuthentication,
        BearerAuthenticationAllowInactiveUser,
        SessionAuthenticationAllowInactiveUser,
    )
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MembershipSerializer

    def post(self, request, course_id: str):  # pylint: disable=unused-argument
        """POST request handler for the team membership view."""
        field_errors = {}

        team_id = request.data.get("team_id")
        usernames = request.data.get("usernames")

        if not team_id:
            field_errors["team_id"] = "The [team_id] query parameter is required."

        if not usernames:
            field_errors["usernames"] = "The [usernames] query parameter is required."

        if field_errors:
            return api_field_errors(field_errors)

        team = get_team_by_team_id(team_id=team_id)
        if not team:
            return api_field_errors(
                {"team_id": f"The supplied {team_id=} does not exists."},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if not has_specific_team_access(request.user, team):
            return api_error(
                f"The {request.user=} do not have access to the specified team.",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        if not can_user_modify_team(request.user, team):
            return api_error(
                f"The {request.user=} can't join an instructor managed team.",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        course_block = modulestore().get_course(team.course_id)

        max_team_size = course_block.teams_configuration.calc_max_team_size(
            team.topic_id
        )
        if (
            max_team_size is not None
            and team.users.exclude(username__in=usernames).count() + len(usernames)
            > max_team_size
        ):
            return api_error(
                f"The {team_id=} does not have enough space for the given users."
            )

        memberships = []

        for username in usernames:
            if not has_team_api_access(
                request.user, team.course_id, access_username=username
            ):
                return api_error(
                    (
                        f"The {request.user=} do not have access "
                        "to the Team API for the given course."
                    ),
                    status_code=status.HTTP_403_FORBIDDEN,
                )

            try:
                user = get_user_by_username_or_email(username)
            except User.DoesNotExist:
                return api_field_errors(
                    {"usernames": f"The {username=} does not exists."},
                    status_code=status.HTTP_404_NOT_FOUND,
                )

            try:
                membership = team.add_user(user)
            except AlreadyOnTeamInTeamset:
                old_membership = (
                    CourseTeamMembership
                    .objects.filter(
                        user=user,
                        team__course_id=team.course_id,
                        team__topic_id=team.topic_id,
                    )
                    .first()
                )
                old_membership.delete()
                membership = team.add_user(user)
            except NotEnrolledInCourseForTeam:
                return api_field_errors(
                    {
                        "usernames": (
                            f"The {username=} is not enrolled in "
                            "the course associated with this team."
                        )
                    },
                )

            serializer = self.get_serializer(instance=membership)
            memberships.append(serializer.data)

        return Response({"memberships": memberships}, status=status.HTTP_201_CREATED)
