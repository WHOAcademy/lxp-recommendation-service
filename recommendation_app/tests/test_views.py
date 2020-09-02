from rest_framework.test import APITestCase
from django.urls import reverse

class TestRecommendationView(APITestCase):

    def test_get_all(self):
        url = reverse("list-recommendations", args=['ce395dc2-f89b-44ce-9e12-20d4e99f3d6a'])
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
