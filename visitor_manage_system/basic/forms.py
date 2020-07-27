from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import validators



def checkforpeople(value):
    if value>5:
        raise forms.ValidationError("residents are more than allowed")


class HostForm(ModelForm):
    no_of_people=forms.IntegerField(validators=[checkforpeople])
    
    class Meta:
        model = Host
        fields = '__all__'
        exclude = ['user']




class createuserform(UserCreationForm):

    class Meta:
        model=User
        fields=['username','email','password1','password2']




class VisitorForm(ModelForm):
    class Meta:
        model = Visitor
        fields = '__all__'
        exclude = ['user']
        
class VisitDetailsForm(ModelForm):
    class Meta:
        model = VisitDetails
        fields = '__all__'


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields ='__all__'

class EventVisitorForm(ModelForm):
    class Meta:
        model = EventVisitor
        fields = '__all__'