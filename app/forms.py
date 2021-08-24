from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
       # email = forms.EmailField(max_length=100)
       number = forms.IntegerField()
       class Meta:
              model = User
              fields = ["username", "email", "password1", "password2","number"]

class ProfileForm(forms.ModelForm):
       class Meta:
            model = Profile
            fields = ['user', 'bio', 'state', 'city', 'birth_date', 'mobile', 'profile_image' ]
