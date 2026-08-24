from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterUserForm(UserCreationForm):
    human_name = forms.CharField(max_length=30, required=False)
    human_surname = forms.CharField(max_length=30, required=False)


    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2',
            'human_name',
            'human_surname',
        ]