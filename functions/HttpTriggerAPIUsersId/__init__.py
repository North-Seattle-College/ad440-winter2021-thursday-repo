import logging
import pyodbc
import os
import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    data = ''
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
            "issue",
            status_code=400
        )
    else:
        # query database
        with pyodbc.connect(connectionString) as conn:

            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM users WHERE userId={}".format(id))

                columns = [column[0] for column in cursor.description]
                data = dict(zip(columns, cursor.fetchone()))

                if not data:
                    return func.HttpResponse(
                        "not found.",
                        status_code=404
                    )
                else:
                    return func.HttpResponse(
                        json.dumps(data),
                        status_code=201,
                        mimetype="application/json"
                    )
                    # return func.HttpResponse(
                    #     json.dumps({"userId": row.userId, "firstName": row.firstName,
                    #                 "lastName": row.lastName, "email": row.email, "deleted": row.deleted}),
                    #     status_code=201
                    # )
