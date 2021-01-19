import logging
import pypyodbc
import os
import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
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
            "Bad Request",
            status_code=400
        )
    else:
        try:
            with pypyodbc.connect(connectionString) as conn:
                return execute_query(conn, id)
        except pypyodbc.DatabaseError as e:
            if e.args[0] == '28000':
                return func.HttpResponse(
                    "Unauthorized",
                    status_code=403
                )


def execute_query(conn, id):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM users WHERE userId={}".format(id))
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
                json.dumps(data),
                status_code=200,
                mimetype="application/json"
            )
