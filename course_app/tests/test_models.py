from datetime import datetime

from django.db import DataError, IntegrityError
from django.test import SimpleTestCase, TestCase
from course_app.models import CourseModel


class TestCourseModel(TestCase):

    def test_create_course(self):
        CourseModel.objects.create(title="Title", description="This is a description", duration_seconds=1200, creation_date=datetime.now(), last_mod_date=datetime.now())

    def test_get_all(self):
        CourseModel.objects.create(title="Title1", description="This is a description", duration_seconds=1200, creation_date=datetime.now(), last_mod_date=datetime.now())
        CourseModel.objects.create(title="Title2", description="This is a description", duration_seconds=1200, creation_date=datetime.now(), last_mod_date=datetime.now())
        CourseModel.objects.create(title="Title3", description="This is a description", duration_seconds=1200, creation_date=datetime.now(), last_mod_date=datetime.now())

        roles = CourseModel.objects.all()
        self.assertEqual(len(roles), 3)

    def test_role_obj(self):
        CourseModel.objects.create(title="Title", description="This is a description", duration_seconds=1200, creation_date=datetime.now(), last_mod_date=datetime.now())
        course = CourseModel.objects.all()[0]
        self.assertTrue(isinstance(course, CourseModel))
        self.assertEqual(course.title, "Title")
        self.assertEqual(course.duration_seconds, 1200)


    def test_title_max_length(self):
        with self.assertRaises(DataError):
            title = "Title" * 200
            CourseModel.objects.create(title=title, description="This is a description", duration_seconds=1200, creation_date=datetime.now(), last_mod_date=datetime.now())