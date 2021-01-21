import logging
import pypyodbc
import os
import azure.functions as func
import datetime
import json
import time


# to handle datetime with JSON
# It serialize datetime by converting it into string
def default(dateHandle):
    if isinstance(dateHandle, (datetime.datetime, datetime.date)):
        return dateHandle.isoformat()


def main(req: func.HttpRequest) -> func.HttpResponse:

    # define the server and database names
    server = os.environ["ENV_DATABASE_SERVER"]
    database = os.environ["ENV_DATABASE_NAME"]
    username = os.environ["ENV_DATABASE_USERNAME"]
    password = os.environ["ENV_DATABASE_PASSWORD"]

    # define the connection string
    driver = '{ODBC Driver 17 for SQL Server}'
    cnxn = "Driver={};Server={};Database={};Uid={};Pwd={};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;".format(
        driver, server, database, username, password)

    user_id = req.route_params.get('userId')

    if not user_id:
        return func.HttpResponse('Bad Request', status_code=400)
    else:
        try:
            with pypyodbc.connect(cnxn) as conn:
                return tasks_query(conn, user_id)
        except pypyodbc.DatabaseError as err:
            if err.args[0] == '28000':
                return func.HttpResponse(
                    "Unauthorized User",
                    status_code=403
                )

# create the connection cursor


def tasks_query(conn, user_id):
    # create the query
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM tasks WHERE userId={}".format(user_id))
        row = list(cursor.fetchall())
        logging.info(row)
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
