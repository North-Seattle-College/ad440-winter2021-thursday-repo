import logging
import pypyodbc
import os
import azure.functions as func
import json

# This is the Http Trigger for Users/userId
# It connects to the db and retrives the users added to the db by userId
# Additional work to be done:
# Add Http Response for UPDATE, DELETE, POST


def main(req: func.HttpRequest) -> func.HttpResponse:
    db_server = os.environ["ENV_DATABASE_SERVER"]
    db_name = os.environ["ENV_DATABASE_NAME"]
    db_username = os.environ["ENV_DATABASE_USERNAME"]
    db_password = os.environ["ENV_DATABASE_PASSWORD"]
    driver = '{ODBC Driver 17 for SQL Server}'
    connectionString = "Driver={};Server={};Database={};Uid={};Pwd={};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;".format(
        driver, db_server, db_name, db_username, db_password)

    # This gets the userId from the query string
    id = req.route_params.get('userId')
    if not id:
        # If no userId is supplied http response -> Bad Request
        return func.HttpResponse(
            "Bad Request",
            status_code=400
        )
    else:
        try:
            with pypyodbc.connect(connectionString) as conn:
                return get_user_by_id(conn, id)
        except pypyodbc.DatabaseError as e:
            # This code is returned by pypyodbc meaning Unautroized when a bad password is supplied etc
            # Adddtional error handeling will need to be implemented, maybe in srpint 2
            if e.args[0] == '28000':
                return func.HttpResponse(
                    "Unauthorized",
                    status_code=403
                )


def get_user_by_id(conn, id):
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
            # This will convert the results from the query into json properties.
            # More information can be found on the link below:
            # https://stackoverflow.com/questions/16519385/output-pyodbc-cursor-results-as-python-dictionary/16523148#16523148
            columns = [column[0] for column in cursor.description]
            data = dict(zip(columns, row))

            return func.HttpResponse(
                json.dumps(data),
                status_code=200,
                mimetype="application/json"
            )
