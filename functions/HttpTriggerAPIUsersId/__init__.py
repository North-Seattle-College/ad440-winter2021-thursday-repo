import logging
import pyodbc
import os
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    db_server = os.environ["ENV_DATABASE_SERVER"]
    db_name = os.environ["ENV_DATABASE_NAME"]
    db_username = os.environ["ENV_DATABASE_USERNAME"]
    db_password = os.environ["ENV_DATABASE_PASSWORD"]
    driver = '{ODBC Driver 17 for SQL Server}'
    connectionString = "Driver={};Server={};Database={};Uid={};Pwd={};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;".format(
        driver, db_server, db_name, db_username, db_password)

    id = req.params.get('id')
    if not id:
        return func.HttpResponse(
            "not found.",
            status_code=404
        )
    else:
        # query database

        with pyodbc.connect(connectionString) as conn:

            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM users WHERE userId={}".format(id))
                row = cursor.fetchone()
                while row:
                    print(str(row[0]) + " " + str(row[1]))
                    row = cursor.fetchone()
        return func.HttpResponse(
            "Data goes here",
            status_code=200
        )
