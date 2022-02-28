from django import forms
from django.contrib.auth import models


class AccountsForm(forms.ModelForm):

    first_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = models.User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password'
        ]
