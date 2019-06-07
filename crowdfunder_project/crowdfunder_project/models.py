from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    budget = models.IntegerField()
    owner = models.CharField(max_length=255)
    image = models.URLField(max_length=255, null=True)


class Backer(models.Model):
    name = models.CharField(max_length=255)
    projects = models.ManyToManyField(Project, related_name='backers')
    