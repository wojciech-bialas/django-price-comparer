from django import forms
from django.contrib.auth import models


class AccountsForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password'
        ]
