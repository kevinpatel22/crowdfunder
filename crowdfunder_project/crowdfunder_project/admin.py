from django.contrib import admin
from django.contrib.auth.models import User
from .models import * 


admin.site.register(Category)
admin.site.register(Project)
admin.site.register(Comment)
admin.site.register(Reward)
admin.site.register(Donation)