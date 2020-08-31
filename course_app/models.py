from django.db import models
from django.conf import settings


class RoleModel(models.Model):
    name = models.CharField(max_length=45, unique=True)
    slug = models.SlugField(max_length=64, unique=True)


class SkillModel(models.Model):
    name = models.CharField(max_length=45, unique=True)
    slug = models.SlugField(max_length=64, unique=True)
    roles = models.ManyToManyField(to=RoleModel)


class CourseTopicModel(models.Model):
    name = models.CharField(max_length=45)
    description = models.TextField()
    synonyms = models.CharField(max_length=100)
    parent = models.ForeignKey(to='self', on_delete=models.SET_NULL, null=True, blank=True)


class CourseModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration_seconds = models.IntegerField()
    creation_date = models.DateTimeField()
    last_mod_date = models.DateTimeField()
    course_topics = models.ManyToManyField(to=CourseTopicModel)
    # TO BE BETTER IMPLEMENTED:
    novice_skills = models.ManyToManyField(to=SkillModel, related_name="novice_skills", blank=True)
    intermediate_skills = models.ManyToManyField(to=SkillModel, related_name="intermediate_skills", blank=True)
    expert_skills = models.ManyToManyField(to=SkillModel, related_name="expert_skills", blank=True)

    def __str__(self):
        return self.title