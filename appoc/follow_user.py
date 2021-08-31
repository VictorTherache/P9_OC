from django import forms
from django.forms import ModelForm

from .models import *

class FollowUser(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = []

