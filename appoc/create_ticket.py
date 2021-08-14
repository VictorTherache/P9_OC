from django import forms
from django.forms import ModelForm

from .models import *

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
