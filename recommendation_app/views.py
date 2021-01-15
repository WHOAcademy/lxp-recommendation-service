from logging import getLogger

from django.conf import settings
from django.http import HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from requests import codes
from requests import get as requests_get
from rest_framework import views
from rest_framework.response import Response

from .constants import constants
from .serializers import RecommendationSerializer
from .recommendation_utils import arrange_content_metadata, \
    get_top_recommendations

logger = getLogger("recommendation")


class RecommendationsView(views.APIView):
    """
    Use this endpoint to GET all recommended courses.
    """

    # caching the response of the requested view method:
    @method_decorator(cache_page(constants['CACHE_TTL']['SHORT']))
    def get(self, request, keycloak_id):

        # TODO: authenticate the user with Keycloak service

        # fetching user metadata: --------------------------------------------

        # sending request to corresponding microservice:
        profile_service_api_url = settings.LXP_PROFILE_SERVICE + \
            '/api/v1/skills-and-topics/' + keycloak_id
        # https://lxp-profile-service-labs-staging.apps.who.emea-2.rht-labs.com/api/v1/profiles/0c6d2004-5cd2-413d-84e3-03dc3af43c2e
        logger.info(profile_service_api_url)
        response = requests_get(profile_service_api_url)
        if response.status_code != codes.ok:
            return HttpResponseBadRequest('Invalid keycloak_id')
        logger.info(response)
        response = response.json()

        # user skill expertise levels:
        user_skill_id_2_level_id_dict = \
            {int(k): v for k, v in response['possessed skill levels'].items()}

        # user topics of interest:
        user_topics_of_interest = response['topics of interest']

        # fetching metadata of all modules: ----------------------------------

        # sending request to corresponding microservice:
        course_service_api_url = settings.LXP_COURSE_SERVICE + \
            '/api/mocked-modules-req-skills-awa-skills-and-topics'
        logger.info(course_service_api_url)
        response = requests_get(course_service_api_url)
        logger.info(response)
        response = response.json()

        # module metadata of interest for building learning pathways:
        module_id_2_required_skill_2_level_dicts, \
            module_id_2_awarded_skill_2_level_dicts, \
            module_id_2_contained_topic_ids_dict, \
            module_ids = arrange_content_metadata(
                module_json_content=response
            )

        # Get the recommended courses
        recommended_module_ids = get_top_recommendations(
            module_id_2_required_skill_2_level_dicts=\
                module_id_2_required_skill_2_level_dicts,
            module_id_2_awarded_skill_2_level_dicts=\
                module_id_2_awarded_skill_2_level_dicts,
            module_id_2_contained_topic_ids_dict=\
                module_id_2_contained_topic_ids_dict,
            module_ids=module_ids,
            user_skill_id_2_level_id_dict=user_skill_id_2_level_id_dict,
            user_topics_of_interest=user_topics_of_interest,
            n_top=3
        )

        # TODO: pass also module information - taken from the course service -
        # to be displayed in addition to module ids representing 
        # recommendations

        data = []
        for module_id in recommended_module_ids:
            obj = {
                "id": module_id,
                "title": "Lorem Ipsum",
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                "duration_seconds": 18000,
                "creation_date": "2020-07-13T12:45:26.401000Z",
                "last_mod_date": "2020-08-11T10:38:29Z"
            }
            data.append(obj)

        results = RecommendationSerializer(data, many=True).data
        return Response(results)
