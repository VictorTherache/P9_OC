from django import forms
from django.forms import ModelForm

from .models import *

class ReviewForm(forms.ModelForm):
    title= forms.CharField(widget= forms.TextInput(attrs={'placeholder':'Add new task...'}))
    class Meta:
        model = Review
        fields = '__all__'