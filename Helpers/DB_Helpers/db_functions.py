from django.db import connection
import sqlalchemy as db
from sqlalchemy import create_engine, orm
from sqlalchemy.schema import FetchedValue
import mysql.connector
import json
import numpy as np
from Helpers.ExceptionLogging.exception_logging import UberExceptionLogging

UberLogString = []

#Create the Instance of UberExceptionLogging Functions 
objUberExceptionLogging = UberExceptionLogging()

#Load Exception Messages
ExceptionMessages = objUberExceptionLogging.load_exception_success("Exception")

#Load the Success Messages
SuccessMessages = objUberExceptionLogging.load_exception_success("Success")


class DBInterations:
    def __init__(self):
        try:
            #Get the fields of the Database Configuration from the Config File
            DBConfig = open('../Helpers/DB_Helpers/db_config.json')
            dbconf = json.load(DBConfig)

            global DBConnector, UserName, Password, ServerOrEndPoint, DatabaseName, AuthenticationPlugin, engine
            DBConnector = dbconf["DBConfigs"]["mysql"]["DBConnecter"]
            UserName = dbconf["DBConfigs"]["mysql"]["UserName"]
            Password = dbconf["DBConfigs"]["mysql"]["Password"]
            ServerOrEndPoint = dbconf["DBConfigs"]["mysql"]["ServerOrEndPoint"]
            DatabaseName = dbconf["DBConfigs"]["mysql"]["DatabaseName"]
            AuthenticationPlugin = dbconf["DBConfigs"]["mysql"]["AuthPlugin"]
        except:
            print("ERROR")

    def get_user_credentials(self, app_user):
        user_credentials = {}
        try:
            engine = db.create_engine(f"{DBConnector}://{UserName}:{Password}@{ServerOrEndPoint}/{DatabaseName}?{AuthenticationPlugin}", encoding='utf8')
            connection = engine.connect()
            result= connection.execute(f"SELECT * FROM core_aws_credentials WHERE aws_user = '{app_user}'")
            for row in result:
                user_credentials = row
            
            return user_credentials
        except:
            objUberExceptionLogging.UberLogException(f"ERROR: Connection cannot be established with the database. User credentials can't be fetched from database", False, False) 