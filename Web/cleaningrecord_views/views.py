from django import forms
from django.http import HttpResponse
from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from .forms import FolderForm, LoginForm
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import sys, os
import requests, json
import string, random
import pathlib, datetime

sys.path.append("./../../UberBuild/")
from Helpers.AWS_Helpers.aws_functions import AWSHelperFunctions
from Helpers.General_Helpers.general_functions import GeneralFunctions

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
        haserror = False
        record_form = FolderForm(request.POST, request.FILES)
        errored_dates = []
        objGeneral = GeneralFunctions()
        csv_file = request.FILES['csvupload']
        csv_file_name = f"uber_driving_records_{objGeneral.unique_string(10)}.csv" 
        csv_file_path = objGeneral.handle_uploaded_file(csv_file, csv_file_name)
        errored_dates = objGeneral.validate_csv(csv_file_path)

        if(len(errored_dates) != 0):
            haserror = True
            print(errored_dates)
            return render(request, 'home.html', {'record_form': record_form, 'error_date':errored_dates, 'haserror': haserror})
    
        objaws = AWSHelperFunctions()
        objaws.upload_file_to_s3(csv_file_path)
        
        #obj = UberCleaningRecordBuilder('Test12')
        #obj.execRecordBuilderFunctionality()
        #obj.execRecordBuilderFunctionality()
        #handle_uploaded_file(request.FILES['csvupload'])
        
        #return HttpResponseRedirect('/about/')
        
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