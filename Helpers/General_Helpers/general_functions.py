import datetime, json
import pandas as pd
import string, random, os


class GeneralFunctions:

    def __init__(self):
        try:
            #Get the fields of the Database Configuration from the Config File
            GeneralConfig = open('../Helpers/General_Helpers/general_config.json')
            general_conf = json.load(GeneralConfig)

            global DateFormat
            DateFormat = general_conf["General_Configs"]["DateFormat"]
        except:
            print("ERROR")

    
    def valid_date(self, date_str):
        date_format = DateFormat
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