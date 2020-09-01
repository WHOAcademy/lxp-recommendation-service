from rest_framework.test import APITestCase
from django.urls import reverse

class TestRecommendationView(APITestCase):

    def test_get_all(self):
        url = reverse("list-recommendations")
        response = self.client.get(url + '?keycloak_id=123', format='json')
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.content, b'OK')