from django import forms
from django.forms import ModelForm

from .models import *

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'headline', 'body']