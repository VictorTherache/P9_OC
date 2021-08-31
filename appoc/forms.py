from appoc.models import Review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CreateReviewForm(forms.Form):
    book_title = forms.CharField(max_length=100)
    book_description = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField()
    review_title = forms.CharField(max_length=100)
    rating = forms.IntegerField(min_value=0, max_value=5)
    review_commentary = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Review
        fields = '__all__'
