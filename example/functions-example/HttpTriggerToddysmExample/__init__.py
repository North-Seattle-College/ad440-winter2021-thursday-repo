import logging
import os
import pyodbc

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    #db_username = os.environ["ENV_DATABASE_USERNAME"]
    #db_password = os.environ["ENV_DATABASE_PASSWORD"]

    conn_string = "Driver={ODBC Driver 17 for SQL Server};Server=tcp:nsc-sqlsrv-usw2-sqltest.database.windows.net,1433;Database=nsc-sqldb-usw2-sqltest;Uid=sqladmin;Pwd=Wm27H#$%imy5dnTkWMYWlXhTy91O;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

    with pyodbc.connect(conn_string) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT taskId, taskUserId, title, taskDescription, completed FROM Tasks")
            rows = cursor.fetchall()
        tasks = []
        for row in rows:
            tasks.append(list(row))

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('test_string')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
