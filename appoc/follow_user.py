from django import forms
from .models import UserFollows


class FollowUser(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = []
