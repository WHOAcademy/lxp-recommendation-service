from django.core.cache import cache
from rest_framework import generics

from course_app import serializers, models
from course_app.constants import constants


class CourseListView(generics.ListAPIView):
    """
    Use this endpoint to GET all courses.
    """
    model = models.CourseModel
    serializer_class = serializers.CourseSerializer
    cache_key = 'course-list'

    def get_queryset(self):
        queryset = cache.get(self.cache_key, None)
        if queryset:
            return queryset
        else:
            queryset = self.model.objects.all()
            cache_ttl = constants['CACHE_TTL']['SHORT']
            cache.set(self.cache_key, queryset, timeout=cache_ttl)
            return queryset


class CourseDetailsView(generics.RetrieveAPIView):
    """
    Use this endpoint to GET only one course's details, based on its id.
    """
    lookup_field = 'id'
    model = models.CourseModel
    serializer_class = serializers.CourseSerializer
    cache_key = 'course-list'
    
    def get_queryset(self):
        queryset = cache.get(self.cache_key, None)
        if queryset:
            return queryset
        else:
            queryset = self.model.objects.all()
            cache_ttl = constants['CACHE_TTL']['SHORT']
            cache.set(self.cache_key, queryset, timeout=cache_ttl)
            return queryset


class CourseTopicsAndSkillsListView(generics.ListAPIView):
    """
    Use this endpoint to GET all courses' topics and skills, without additional fields.
    """
    model = models.CourseModel
    serializer_class = serializers.CourseTopicsAndSkillsSerializer
    cache_key = 'course-list'

    def get_queryset(self):
        queryset = cache.get(self.cache_key, None)
        if queryset:
            return queryset
        else:
            queryset = self.model.objects.all()
            cache_ttl = constants['CACHE_TTL']['SHORT']
            cache.set(self.cache_key, queryset, timeout=cache_ttl)
            return queryset   