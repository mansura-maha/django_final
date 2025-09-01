from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Blog, Rating

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    is_author = forms.BooleanField(required=False, label='Register as Author')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_author']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic', 'social_link']

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'category', 'body']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['value']
