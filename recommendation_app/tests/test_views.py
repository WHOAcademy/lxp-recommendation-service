from rest_framework.test import APITestCase
from django.urls import reverse
from django.conf import settings

import requests

class TestRecommendationView(APITestCase):

    def get_valid_keycloak_id(self):
        # Get a valid keycloak id
        # https://test-lxp-profile-service-labs-test.apps.who.lxp.academy.who.int/api/v1/profiles
        profile_service_url = settings.LXP_PROFILE_SERVICE + '/api/v1/profiles'

        profile_service_response = requests.get(profile_service_url)
        if profile_service_response.status_code != requests.codes.ok:
            return None

        profiles = profile_service_response.json()

        for profile in profiles:
            return  profile['keycloak_id']

    def test_get_all(self):
        keycloak_id = self.get_valid_keycloak_id()

        url = reverse("list-recommendations", args=[keycloak_id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data) # checking at least one course is recommended

        # TODO Not sure what's the value of the below lines?
        # course_1 = response.data[0]

        # time_format = '%Y-%m-%dT%H:%M:%S.%fZ'

        # self.assertEquals(course_1.title, response.data[0]["title"])
        # self.assertEquals(course_1.description, response.data[0]["description"])
        # self.assertEquals(course_1.duration_seconds, response.data[0]["duration_seconds"])
        # self.assertEquals(course_1.creation_date.strftime(time_format), response.data[0]["creation_date"])
        # self.assertEquals(course_1.last_mod_date.strftime(time_format), response.data[0]["last_mod_date"])
