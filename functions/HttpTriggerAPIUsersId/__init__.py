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

    id = req.params.get('id')
    if not id:
        return func.HttpResponse(
            "not found.",
            status_code=404
        )
    else:
        # query database
        with pyodbc.connect('DRIVER='+driver+';SERVER='+db_server+';PORT=1433;DATABASE='+db_name+';UID=' + db_username+';PWD=' + db_password) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT TOP 3 name, collation_name FROM sys.databases")
                row = cursor.fetchone()
                while row:
                    print(str(row[0]) + " " + str(row[1]))
                    row = cursor.fetchone()
        return func.HttpResponse(
            "Data goes here",
            status_code=200
        )
