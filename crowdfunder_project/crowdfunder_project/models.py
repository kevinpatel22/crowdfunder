from django.db import models
from django.contrib.auth.models import User
from datetime import timezone, datetime

class Category(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return f'-~-~- {self.name} -~-~-'

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    budget = models.IntegerField()
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='projects')
    image = models.URLField(max_length=255, null=True)
    start_dtime = models.DateTimeField(default=datetime.now)
    end_dtime = models.DateTimeField(null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='projects', null=True)

class Comment(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField(blank=True,default='when blank, save this instead!')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='comments')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')

class Reward(models.Model):
    name = models.CharField(max_length=255)
    message = models.TextField(null=True, max_length=2000)
    pledge_for = models.CharField(max_length=10)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='rewards')

class Donation(models.Model):
    ily_message = models.CharField(max_length=20, default='I Love You Too!')
    amount = models.IntegerField()
    donator = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='charities', null=True)
    reward = models.ForeignKey(Reward, on_delete=models.SET_NULL, related_name='donations', null=True)

class Update(models.Model):
    message = models.TextField()
    title = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='updates')

