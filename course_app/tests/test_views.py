from datetime import datetime

from django.test import SimpleTestCase, TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from course_app.models import CourseModel


class TestSkillView(APITestCase):

    def test_get_all(self):
        course_1 = CourseModel.objects.create(title="Title1", description="This is a description", duration_seconds=1200,
                                   creation_date=datetime.now(), last_mod_date=datetime.now())
        course_2 = CourseModel.objects.create(title="Title2", description="This is a description", duration_seconds=1200,
                                   creation_date=datetime.now(), last_mod_date=datetime.now())

        url = reverse("list-courses")
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        time_format = '%Y-%m-%dT%H:%M:%S.%fZ'

        self.assertEquals(course_1.title, response.data[0]["title"])
        self.assertEquals(course_1.description, response.data[0]["description"])
        self.assertEquals(course_1.duration_seconds, response.data[0]["duration_seconds"])
        self.assertEquals(course_1.creation_date.strftime(time_format), response.data[0]["creation_date"])
        self.assertEquals(course_1.last_mod_date.strftime(time_format), response.data[0]["last_mod_date"])

        self.assertEquals(course_2.title, response.data[1]["title"])
        self.assertEquals(course_2.description, response.data[1]["description"])
        self.assertEquals(course_2.duration_seconds, response.data[1]["duration_seconds"])
        self.assertEquals(course_2.creation_date.strftime(time_format), response.data[1]["creation_date"])
        self.assertEquals(course_2.last_mod_date.strftime(time_format), response.data[1]["last_mod_date"])