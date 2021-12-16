import json
import boto3
import os
from Helpers.DB_Helpers.db_functions import DBInterations
from Helpers.ExceptionLogging.exception_logging import UberExceptionLogging

#Create the Instance of UberExceptionLogging Functions 
objUberExceptionLogging = UberExceptionLogging()

class AWSHelperFunctions:
    
    def __init__(self):
        try:
            
            #Get download path of the CSV file to begin the cleaning record process
            AWSConfig = open('../Helpers/AWS_Helpers/aws_config.json')
            awsconfig = json.load(AWSConfig)
            app_user = awsconfig["configs"]["User"]

            #Get configurations from database for AWS
            objDB = DBInterations()
            cleaningRecCredentials = objDB.get_user_credentials(app_user)
            
            #Load configurations to necessary variables
            global CleanRecKey, CleanRecSec, CleanRecHome, CleanRecFolder, CSVDownloadPath
            CleanRecKey = cleaningRecCredentials["aws_key"]
            CleanRecSec = cleaningRecCredentials["aws_secret_key"]
            CleanRecHome = cleaningRecCredentials["aws_home"]
            CleanRecFolder = cleaningRecCredentials["aws_bucket_name"]

        except:
            objUberExceptionLogging.UberLogException("Can't load the AWS configurations, Please check if the file is in correct location.", True, True)

    #Get the AWS Session for provided AWS Credentials
    def aws_session(self):
        try:
            aws_sess = boto3.session.Session(aws_access_key_id=CleanRecKey,
                                    aws_secret_access_key=CleanRecSec,
                                    region_name=CleanRecHome)
            
            if not aws_sess == None:
                print("AWS Session created successfully!!!")

            return aws_sess

        except:
                objUberExceptionLogging.UberLogException("Can't connect to AWS cloud. Kindly check the credentials again or check the connectivity to Internet", True, True)


    #Upload file to AWS S3 Bucket
    def upload_file_to_s3(self, file_path):
        try:
            session = self.aws_session()
            s3_resource = session.resource('s3')
            file_dir, file_name = os.path.split(file_path)

            bucket = s3_resource.Bucket(CleanRecFolder)
            bucket.upload_file(Filename=file_path, Key=file_name,)
            
        except:
            objUberExceptionLogging.UberLogException("An ERROR occured while uploading the file. Please check if internet is connected or not.", True, True)