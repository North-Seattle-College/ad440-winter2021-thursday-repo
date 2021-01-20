import logging
import pyodbc
import os
import azure.functions as func
import datetime
import json
import time



# to handle datetime with JSON object
def default(o):
    if isinstance(o, (datetime.datetime, datetime.date)):
        return o.isoformat()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # define the server and database names
    server = os.environ["ENV_DATABASE_SERVER"]
    database = os.environ["ENV_DATABASE_NAME"]
    username = os.environ["ENV_DATABASE_USERNAME"]
    password = os.environ["ENV_DATABASE_PASSWORD"]
    
    # define the connection string
    driver = '{ODBC Driver 17 for SQL Server}'
    cnxn = "Driver={};Server={};Database={};Uid={};Pwd={};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;".format(
        driver, server, database, username, password)
    
   
    id = 1

    if not id:
        return func.HTTPResponse('Bad Request', status_code=400 )
    else:
        try:
            with pyodbc.connect(cnxn) as conn:
                return tasks_query(conn, id)
        except pyodbc.DatabaseError as err:
            if err.args[0] == '28000':
                return func.HttpResponse(
                    "Unauthorized User",
                    status_code=403 
                )

# create the connection cursor
def tasks_query(conn, id):
    # create the query
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
            return func.HttpResponse(
                json.dumps(data, default=default),
                status_code=200,
                mimetype="application/json"
            )       
 

