from django import forms
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from .forms import LoginForm

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'home.html'

class AboutPageView(TemplateView):
    template_name = 'about.html'

class LoginPageView(TemplateView):
    template_name = 'login.html'
    
    def post(self, request, *args, **kwargs):
        username = ""
        if(request.method == 'POST'):
            MyLoginForm = LoginForm(request.POST)

            if(MyLoginForm.is_valid()):
                username = MyLoginForm.cleaned_data['email'] 

        else:
            MyLoginForm = LoginForm()

        return render(request, 'home.html', {'username': username})