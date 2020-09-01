from django.conf import settings
import logging
import requests

from rest_framework import views
from rest_framework.response import Response

from .serializers import RecommendationSerializer
from .recommendation_utils import get_recommended_courses

logger = logging.getLogger("recommendation")


class RecommendationListView(views.APIView):
    """
    Use this endpoint to GET all recommended courses.
    """

    def pasta(self):
        data = {"course_topics":[36, 44],"novice_skills":[21, 19],"intermediate_skills":[],"expert_skills":[]}
        return data

    def get(self, request, keycloak_id):
        # TODO: authenticate the user with Keycloak service

        # Get user profile skills and interests
        # https://lxp-profile-service-labs-staging.apps.who.emea-2.rht-labs.com/api/v1/profiles/0c6d2004-5cd2-413d-84e3-03dc3af43c2e
        profile_service_url = settings.LXP_PROFILE_SERVICE + '/api/v1/profiles/' + keycloak_id
        logger.info(profile_service_url)

        # TODO: Handle invalid keycloak_id
        user_topics_and_skills = requests.get(profile_service_url).json()
        logger.info(user_topics_and_skills)
        user_topics_and_skills = self.pasta()

        # Get Course details
        course_service_url = settings.LXP_COURSE_SERVICE + '/api/courses-topics-and-skills'
        logger.info(course_service_url)

        courses_topics_and_skills = requests.get(course_service_url).json()

        # Get the recommended courses
        recommended_courses = get_recommended_courses(courses_topics_and_skills, user_topics_and_skills)

        data= [
            {"data": "10"},
            {"data": keycloak_id},
            {"data": course_service_url + ' '.join([str(x) for x in recommended_courses])}
        ]

        results = RecommendationSerializer(data, many=True).data
        return Response(results)


    # update the algorithm to filter down courses - for profile and course api changes
    # apply the algorithm to filter down courses - no problem for order, present all top ones
    # update the serializer for the response format
    # pass courses back to front-end
    # Update the test cases - refer course service
    # Handle invalid keycloak_id
