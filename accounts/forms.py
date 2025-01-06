from django import forms
from django.contrib.auth import models
from django.contrib.auth.hashers import make_password


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

    def save(self, commit=True):
        user = super().save(commit=False)  # Get the user instance without saving
        user.password = make_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()  # Save the user to the database
        return user
