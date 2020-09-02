from django.conf import settings
from django.http import HttpResponseBadRequest
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

    def get(self, request, keycloak_id):
        # TODO: authenticate the user with Keycloak service

        # Get user profile skills and interests
        # https://lxp-profile-service-labs-staging.apps.who.emea-2.rht-labs.com/api/v1/profiles/0c6d2004-5cd2-413d-84e3-03dc3af43c2e
        profile_service_url = settings.LXP_PROFILE_SERVICE + '/api/v1/profiles/' + keycloak_id
        logger.info(profile_service_url)

        profile_service_response = requests.get(profile_service_url)
        if profile_service_response.status_code != requests.codes.ok:
            return HttpResponseBadRequest('Invalid keycloak_id')

        user_topics_and_skills = profile_service_response.json()
        logger.info(user_topics_and_skills)

        # Get Course details
        course_service_url = settings.LXP_COURSE_SERVICE + '/api/courses-topics-and-skills'
        logger.info(course_service_url)

        courses_topics_and_skills = requests.get(course_service_url).json()

        # Get the recommended courses
        recommended_courses = get_recommended_courses(courses_topics_and_skills, user_topics_and_skills, n_top = 7)

        data = []
        for course in recommended_courses:
            obj = {
                "id": course['id'],
                "title": course['title'],
                "description": "Lorem Ipsum", # TODO: update the course service to get this data
                "duration_seconds": 18000, # TODO: update the course service to get this data
                "creation_date": "2020-07-13T12:45:26.401000Z", # TODO: update the course service to get this data
                "last_mod_date": "2020-08-11T10:38:29Z" # TODO: update the course service to get this data
            }
            data.append(obj)

        results = RecommendationSerializer(data, many=True).data
        return Response(results)
