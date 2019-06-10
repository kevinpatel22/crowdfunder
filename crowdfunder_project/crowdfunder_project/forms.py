from datetime import datetime, date, timedelta
from django.utils import timezone
from crowdfunder_project.models import *
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.forms import (CharField, DateField, IntegerField, HiddenInput, 
      Form, ModelForm, DateTimeField, SplitDateTimeWidget, SplitDateTimeField,  
     PasswordInput, Textarea, TimeField)
from django.core.validators import MinValueValidator

class ProjectForm(ModelForm):
    budget = IntegerField(validators=[MinValueValidator(10)] )
    start_dtime = DateField()
    end_dtime = DateField()

    class Meta:
        model = Project
        fields = ['category', 'title', 'description', 'budget', 'start_dtime', 'end_dtime', 'image']

    def clean(self):
        data = self.cleaned_data
        if data['end_dtime'] and data['end_dtime'] < data['start_dtime']:
            raise ValidationError("end_dtime cannot be less than start_dtime")
        elif data['start_dtime'] < date(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day):
            raise ValidationError("start_dtime cannot be less than datetime.now()")
        return data


class RewardForm(ModelForm):
    
    pledge_for = IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        model = Reward
        fields = ['name', 'message', 'pledge_for']

class LoginForm(Form):
    username = CharField(label="User Name", max_length=64)
    password = CharField(widget=PasswordInput())

class CommentForm(Form):
    title = CharField(max_length=100)
    message = CharField(max_length=200)

    class Meta:
        model = Comment
        fields = ['title', 'message']

