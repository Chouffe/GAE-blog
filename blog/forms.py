from django import forms
from models import User
from google.appengine.ext import db


class UserForm(forms.Form):
    username = forms.CharField(max_length=25)
    password = forms.CharField(widget=forms.PasswordInput(), min_length=6, max_length=30)
    verif_password = forms.CharField(widget=forms.PasswordInput(), min_length=6, max_length=30)

    def clean_username(self):
        if db.GqlQuery("SELECT * FROM User WHERE username = :1", self.cleaned_data['username']).fetch(1):
            raise forms.ValidationError("Username not available")

        return self.cleaned_data['username']

    def clean_verif_password(self):
        password = self.cleaned_data['password']
        v_password = self.cleaned_data['verif_password']

        if password != v_password:
            raise forms.ValidationError("Passwords are different")
