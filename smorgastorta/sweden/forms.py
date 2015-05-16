from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'type':"text", 'name':"name", 'id':"name", 'placeholder':"Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'type':"password", 'name':"password", 'id':"password", 'placeholder':"Password"}))
