import json
import pypyodbc
import logging
import os
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP Database trigger function processed a request.')
    
    # Database credentials.
    server = os.environ["ENV_DATABASE_SERVER"]
    database = os.environ["ENV_DATABASE_NAME"]
    username = os.environ["ENV_DATABASE_USERNAME"]
    password = os.environ["ENV_DATABASE_PASSWORD"]
    
    # Define driver
    driver = '{ODBC Driver 17 for SQL Server}'
    
    # Define the connection string
    connection_string = "Driver={};Server={};Database={};Uid={};Pwd={};Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=30;".format(driver, server, database, username, password)
    
    # Create a new connection
    try:
        with pypyodbc.connect(connection_string) as conn:
            return select_users_query(conn)
    except pypyodbc.DatabaseError as e:
        if e.args[0] == '28000':
          return func.HttpResponse(
              "Unauthorized",
              status_code=403
          )

# Define query    
def select_users_query(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users")

        # Get users
        users = list(cursor.fetchall())
            
        # Clean up to put them in JSON.
        users = [tuple(user) for user in users]
            
        # Empty data list
        data = []

        columns = [column[0] for column in cursor.description]
        for user in users:
            data.append(dict(zip(columns, user)))
            
        # users = dict(zip(columns, rows))
        return func.HttpResponse(json.dumps(data), status_code=200, mimetype="application/json")