from bs4 import BeautifulSoup
import datetime, json
import pandas as pd
import string, random, os
from os import listdir
import pdftotree
import glob



class GeneralFunctions:

    def __init__(self):
        try:
            #Get the fields of the Database Configuration from the Config File
            global DateFormat, general_conf
            GeneralConfig = open('../Helpers/General_Helpers/general_config.json')
            general_conf = json.load(GeneralConfig)
        except:
            print("ERROR")

    
    def valid_date(self, date_str):
        date_format = self.get_config_values("DateFormat")
        try:
            datetime.datetime.strptime(date_str, date_format)
        except:
            return date_str

    def validate_csv(self, file_name_with_complete_path):
        
        csv_cleaning_records = pd.read_csv(file_name_with_complete_path)
      
        errored_date_list = []
        for cleaning_records_date in csv_cleaning_records["DateTimeTrip"]:
            daterror = self.valid_date(cleaning_records_date)
            if daterror != None:
                errored_date_list.append(daterror)

        return errored_date_list
    
    def handle_uploaded_file(self, f, filename):
        with open(f'../CSV/{filename}', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        return os.path.abspath(f'../CSV/{filename}')
        

    def unique_string(self, length):  
        letters = string.ascii_lowercase # define the specific string  
        # define the condition for random.sample() method  
        result = ''.join((random.sample(letters, length))) 

        return result
    
    def get_config_values(self, config_header):
        config_value = general_conf["General_Configs"][config_header]

        return config_value

    def get_folder_list(self):
        file_folder_list = []
        
        statements_folder = self.get_config_values('StatementsFolder') 
        file_folder_list = os.listdir(statements_folder)
        str_folder_name = ""
        
        for folder in file_folder_list:
            if(os.path.isdir(os.path.join(f'{statements_folder}/{folder}'))):
                str_folder = f"(('{folder}'), ('{folder}')),"
                str_folder_name += str_folder
                
        str_folder_name = eval(str_folder_name)
        print(str_folder_name)
        return str_folder_name

    def formDate(self, row):
        trip_date_time = ""
        if len(row.findChildren()) <= 5:
            getspanchild = row.findChildren()
            tripdatetime = ""
            for gsc in getspanchild:
                tripdatetime += f"{gsc.text},"
                
            tripdatetime1 = tripdatetime.split(',') 
            temp = tripdatetime1[2]
            triptime = temp[:2] + ":" + temp[2:] 
            
            if tripdatetime1[3] == "AM" or tripdatetime1[3] == "PM":
                trip_date_time = f"{tripdatetime1[1]} {tripdatetime1[0]}, 2022 {triptime} {tripdatetime1[3]}"

        return trip_date_time

    def clean_alt_list(self, list_):
        list_ = str(list_)
        list_ = list_.replace('\\x00', '')
        list_ = list_.replace('[', '')
        list_ = list_.replace(']', '')
        list_ = list_.replace("'", "")
        return list_

    def check_pdf_file(self, folder_name):
        statements_folder = self.get_config_values('StatementsFolder') 
        root_file_name = f"{statements_folder}/{folder_name}/*.pdf" 
        pdffiles = glob.glob(root_file_name)
        
        if(not pdffiles):
            return False
        else:
            return True

    def generate_csv_with_trip_datetime(self, folder_name):
        statements_folder = self.get_config_values('StatementsFolder') 
        root_file_name = f"{statements_folder}/{folder_name}/*.pdf" 
        pdffiles = glob.glob(root_file_name)

        root_Uber_Statements_html_path = f"{root_file_name.split('*')[0]}HTML"

        if not os.path.exists(root_Uber_Statements_html_path):
            os.makedirs(root_Uber_Statements_html_path)
            print(f"HTML folder {root_Uber_Statements_html_path} created successfully!!!!")
        else:
            print("HTML folder already exists!!!!")

        htmlfiles = []
        for pdf_file in pdffiles:
            pdf_file_name = pdf_file.split('/')
            html_file_name = f"{root_Uber_Statements_html_path}/{pdf_file_name[len(pdf_file_name) - 1]}".replace("pdf","html")
            htmlfiles.append(html_file_name)
            pdftotree.parse(pdf_file, html_path=f"{html_file_name}", model_type=None, model_path=None, visualize=False)
            if os.path.exists(html_file_name):
                print(f"{html_file_name} created successfully!!!!!")
            else:
                print(f"There was problem while creating {html_file_name}, Please try again!!!!!")

        html_files = htmlfiles

        DateFormat = '%d %b, %Y %I:%M %p'
        data = []
        for html_file in html_files:
            with open(html_file) as fp:
                soup = BeautifulSoup(fp, 'html.parser')
                spans = soup.findAll('span', {'class' : 'ocrx_line'})
                #print(spans)
                for row in spans:
                    if len(row.findChildren()) >= 4:
                        if self.formDate(row) != None and self.formDate(row) != "":
                            data.append([self.formDate(row)])


        root_Uber_Statements_csv_path = f"{root_file_name.split('*')[0]}CSV"

        if not os.path.exists(root_Uber_Statements_csv_path):
            os.makedirs(root_Uber_Statements_csv_path)
            print(f"CSV folder {root_Uber_Statements_csv_path} created successfully!!!!")
        else:
            print("CSV folder already exists!!!!")

        uber_csv_file = f"{root_Uber_Statements_csv_path}/UberTripRecords.csv"


        df = pd.DataFrame({'DateTimeTrip': data})
        df["DateTimeTrip"] = df["DateTimeTrip"].apply(lambda x: self.clean_alt_list(x))
        df.to_csv(uber_csv_file, index=False)

        if os.path.exists(uber_csv_file):
            print(f"{uber_csv_file} created successsfully!!!!!")
        else:
            print(f"{uber_csv_file} can't be created, please try again!!!!!")
