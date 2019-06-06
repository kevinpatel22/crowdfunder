from django.db import models
from django.contrib.auth.models import User


class Owner(models.Model):
    name = models.CharField(max_length=255)

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    budget = models.IntegerField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='projects')
    


class Backer(models.Model):
    name = models.CharField(max_length=255)
    projects = models.ManyToManyField(Project, on_delete=models.CASCADE, related_name='backers')
    