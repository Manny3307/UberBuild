from traceback import print_tb
from django import forms
from django.http import HttpResponse
from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from .forms import FolderForm, LoginForm, PDFToCSVForm
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
        sendfolderandfile = {"folder_name": record_form['foldername'].value(), "csv_file_name": csv_file_name }
        

        if(len(errored_dates) != 0):
            haserror = True
            return render(request, 'home.html', {'record_form': record_form, 'error_date':errored_dates, 'haserror': haserror})
    
        objaws = AWSHelperFunctions()
        successupload = objaws.upload_file_to_s3(csv_file_path)
        print(successupload)
        if successupload == "":
            clean_record_result = requests.post(url = "http://172.21.0.3:8000/api/cleaning_rec/create-records/", data = sendfolderandfile, headers={"Authorization":"Token 2a6f3b67d79712731e228d53df5594075753a9fa" })
            print(f"Status Code = {clean_record_result.status_code}")
        else:
            hasawserror = True
            return render(request, 'home.html', {'record_form': record_form, 'successupload':successupload, 'hasawserror': hasawserror})
    else:
        record_form = FolderForm()
        
    return render(request, 'home.html', {'record_form': record_form})

def pdf_to_csv(request):
    pdf_to_csv_form = PDFToCSVForm(request.POST, request.FILES)
    folder_name = pdf_to_csv_form['foldername'].value()
    
    if request.method == 'POST':
        has_error = False
        objGeneral = GeneralFunctions()
        pdf_exists = objGeneral.check_pdf_file(folder_name)
        if(not pdf_exists):
            print(pdf_exists)
            has_error = True
            error_message = "No PDF file(s) exists in the selected folder. Make sure you have the PDF files in the right and selected the right folder."
            return render(request, 'pdf_to_csv.html', {'pdf_to_csv_form': pdf_to_csv_form, 'has_error': has_error, 'error_message': error_message})
        else:
            success_message = f"UberTripRecord.csv successfully created in {folder_name}"
            is_success = True
            objGeneral.generate_csv_with_trip_datetime(folder_name)
            return render(request, 'pdf_to_csv.html', {'pdf_to_csv_form': pdf_to_csv_form, 'is_success': is_success, 'success_message': success_message})
    else:
        pdf_to_csv_form = PDFToCSVForm()
        
    return render(request, 'pdf_to_csv.html', {'pdf_to_csv_form': pdf_to_csv_form})


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