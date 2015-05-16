from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'type':"text", 'name':"name", 'id':"name", 'placeholder':"Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'type':"password", 'name':"password", 'id':"password", 'placeholder':"Password"}))


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username")
