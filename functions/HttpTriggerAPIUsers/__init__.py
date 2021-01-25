import json
import pyodbc
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
    driver = '{SQL Server}'
    
    # Define the connection string
    connection_string = "Driver={};Server={};Database={};Uid={};Pwd={};Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=30;".format(
        driver, server, database, username, password)
    
    # Create a new connection
    logging.debug("Attempting DB connection!")
    try:
        with pyodbc.connect(connection_string) as conn:
            logging.debug("Connection successful! Attempting to retrieve users.")
            return get_users(conn)
    except pyodbc.DatabaseError as e:
        logging.error("Failed to connect to DB: " + e.args[0])
        logging.debug("Error: " + e.args[1])
        if e.args[0] == '28000':
          return func.HttpResponse(
              "Unauthorized",
              status_code=403
          )

# Define query    
def get_users(conn):
    with conn.cursor() as cursor:
        logging.debug("Using connection cursor to execute query (select all from users)")
        cursor.execute("SELECT * FROM users")

        # Get users
        logging.debug("Fetching all queried information")
        users = list(cursor.fetchall())
            
        # Clean up to put them in JSON.
        users = [tuple(user) for user in users]
            
        # Empty data list
        data = []

        columns = [column[0] for column in cursor.description]
        for user in users:
            data.append(dict(zip(columns, user)))
            
        # users = dict(zip(columns, rows))
        logging.debug("User data retrieved and processed, returning information from get_users function")
        return func.HttpResponse(json.dumps(data), status_code=200, mimetype="application/json")