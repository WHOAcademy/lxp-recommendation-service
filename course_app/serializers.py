from rest_framework import serializers
from .models import CourseModel


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModel
        exclude = ('course_topics', 'novice_skills', 'intermediate_skills', 'expert_skills')


class CourseTopicsAndSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModel
        fields = ['id', 'course_topics', 'novice_skills', 'intermediate_skills', 'expert_skills']
