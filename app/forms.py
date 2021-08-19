from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class SignUpForm(UserCreationForm):
       email = forms.EmailField(max_length=100)
       number = forms.IntegerField()


class ProfileForm(forms.ModelForm):
       class Meta:
            model = Profile
            fields = ['user', 'bio', 'state', 'city', 'birth_date', 'mobile', 'profile_image' ]
