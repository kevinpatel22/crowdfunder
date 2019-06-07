import datetime as dt
from crowdfunder_project.models import *
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.forms import (CharField, DateField, IntegerField,
      Form, ModelForm,
     PasswordInput, Textarea, TimeField)
from django.core.validators import MinValueValidator

class ProjectForm(ModelForm):
    
    # title = forms.CharField()
    # description = forms.CharField()
    budget = IntegerField(validators=[MinValueValidator(1)] )

    class Meta:
        model = Project
        fields = ['owner','title', 'description', 'budget', 'image']


class LoginForm(Form):
    username = CharField(label="User Name", max_length=64)
    password = CharField(widget=PasswordInput())
