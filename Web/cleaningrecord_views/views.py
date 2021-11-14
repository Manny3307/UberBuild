from django import forms
from django.http import HttpResponse
from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from .forms import FolderForm, LoginForm
import sys
sys.path.append("/home/manny/UberBuild/")
from Callable.UberCleaningRecordBuilder import UberCleaningRecordBuilder

# Create your views here.
# Login Page Call
def login_page(request): 
    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            return HttpResponseRedirect('/home/')

    else:
        login_form = LoginForm()

    return render(request, 'login.html', {'login_form': login_form})

# Home Page Call
def home_page(request):
    if request.method == 'POST':
        record_form = FolderForm(request.POST, request.FILES)

        obj = UberCleaningRecordBuilder('Test12')
        obj.execRecordBuilderFunctionality()
        #obj.execRecordBuilderFunctionality()
        #handle_uploaded_file(request.FILES['csvupload'])
        return HttpResponseRedirect('/about/')

    else:
        record_form = FolderForm()

    return render(request, 'home.html', {'record_form': record_form})

def about_page(request):
    manny = 5
    if manny == 4:
        return render(request, 'home.html')
    else:
        return render(request, 'about.html')


def Error404(request):
    return render(request, '404_error.html')

def AppMessage(request):
    return render(request, 'app_message.html')


def handle_uploaded_file(f):
    with open('/home/manny/cleaningrecord/django_test/test.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)