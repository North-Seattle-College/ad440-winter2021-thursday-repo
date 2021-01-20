import logging
import pyodbc
import os
import azure.functions as func
import datetime
import json
from json import JSONEncoder


# date1 = 'June 8, 2011'
# date2 = '08/31/79'
#  date3 = '09-04-1954 02:15:05'

# date1_obj = datetime.strptime(date1, '%B %d, %Y')
# date2_obj = datetime.strptime(date2, '%m/%d/%y')
#  date3_obj = datetime.strptime(date3, '%m-%d-%Y %H:%M:%S')



def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # define the server and database names
    server = os.environ["ENV_DATABASE_SERVER"]
    database = os.environ["ENV_DATABASE_NAME"]
    username = os.environ["ENV_DATABASE_USERNAME"]
    password = os.environ["ENV_DATABASE_PASSWORD"]
    
    # define the connection string
    driver = '{ODBC Driver 17 for SQL Server}'
    connectionString = "Driver={};Server={};Database={};Uid={};Pwd={};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;".format(
        driver, server, database, username, password)
    # create the connection cursor
    # cursor = conn.cursor()
   
    id = 1

    if not id:
        return func.HTTPResponse('Bad Request', status_code=400 )
    else:
        try:
            with pyodbc.connect(connectionString) as conn:
                return execute_query(conn, id)
        except pyodbc.DatabaseError as e:
            if e.args[0] == '28000':
                return func.HttpResponse(
                    "Unauthorized",
                    status_code=403
                )
def execute_query(conn, id):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM tasks WHERE userId={}".format(id))
        row = cursor.fetchone()
        if not row:
            return func.HttpResponse(
                "User not found",
                status_code=404
            )
        else:
            columns = [column[0] for column in cursor.description]
            data = dict(zip(columns, row))
            datetime = {'09-04-1954 02:15:05'}
            return func.HttpResponse(
                json.dumps(data),
                json.dumps(datetime, default=str)
                status_code=200,
                mimetype="application/json"
            )       
 

