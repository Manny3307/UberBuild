from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 100)
    password = forms.CharField(widget = forms.PasswordInput())

