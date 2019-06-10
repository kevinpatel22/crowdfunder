import datetime as dt
from crowdfunder_project.models import *
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.forms import (CharField, DateField, IntegerField, HiddenInput, 
      Form, ModelForm,
     PasswordInput, Textarea, TimeField)
from django.core.validators import MinValueValidator

class ProjectForm(ModelForm):
    
    budget = IntegerField(validators=[MinValueValidator(10)] )

    class Meta:
        model = Project
        fields = ['category', 'title', 'description', 'budget', 'start_dtime', 'end_dtime', 'image']

class RewardForm(ModelForm):
    
    pledge_for = IntegerField(validators=[MinValueValidator(1)])
    # project = CharField(widget=HiddenInput(), required=False)

    class Meta:
        model = Reward
        fields = ['name', 'message', 'pledge_for']

class LoginForm(Form):
    username = CharField(label="User Name", max_length=64)
    password = CharField(widget=PasswordInput())
