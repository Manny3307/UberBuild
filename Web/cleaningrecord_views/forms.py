from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect


class LoginForm(forms.Form):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    rememberme = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), initial=False, required=False)

class FolderForm(forms.Form):
    foldername = forms.CharField(widget=forms.TextInput(attrs={'required': True, 'maxlength': 50, 'id': 'inputLGEx', 'class':'form-control'}))
    csvupload = forms.FileField(widget=forms.FileInput(attrs={'class':'custom-file-input', 'id':'inputGroupFile01', 'name': 'csvupload' , 'onchange':'showSelectedFile()', 'aria-describedby':'inputGroupFileAddon01'}))
    addcomments = forms.CharField(widget=forms.Textarea(attrs={'id':'message', 'name':'message', 'rows':'3', 'class':'form-control md-textarea'}), required=False)
