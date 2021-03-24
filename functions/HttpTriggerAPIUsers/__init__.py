import json
import pyodbc
import logging
import os
import datetime
import redis
import azure.functions as func

USERS_CACHE_KEY = b'users:all'
CACHE_TOGGLE = os.environ["CACHE_TOGGLE"]

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(
        'Python HTTP trigger for /users function is processing a request.')

    # Check request method
    method = req.method
    if not method:
        logging.critical('No method available')
        raise Exception('No method passed')

    # Create a new connection
    logging.debug("Attempting DB connection!")
    try:
        conn = get_db_connection()
    except (pyodbc.DatabaseError, pyodbc.InterfaceError) as e:
        logging.critical("Failed to connect to DB: " + e.args[0])
        logging.info("Error: " + e.args[1])
        return func.HttpResponse(status_code=500)
        
    logging.debug("Connection to DB successful!")

    # If DB doesn't already have a users table, create it
    create_users_table(conn)

    # Initiate connection to Redis Cache
    r = init_redis()

    try:
        # Return results according to the method
        if method == "GET":
            logging.info("Attempting to retrieve users...")
            all_users_http_response = get_users(conn, r, req)
            logging.info("Users retrieved successfully!")
            return all_users_http_response

        elif method == "POST":
            logging.info("Attempting to add user...")
            user_req_body = req.get_json()
            new_user_id_http_response = add_user(conn, user_req_body, r)
            logging.info("User added successfully!")
            return new_user_id_http_response

        else:
            logging.warn(f"Request with method {method} has been recieved, but that is not allowed for this endpoint")
            return func.HttpResponse(status_code=405)

    #displays erros encountered when API methods were called
    except Exception as e:
        return func.HttpResponse("Error: %s" % str(e), status_code=500)
    finally: 
        conn.close()
        logging.debug('Connection to DB closed')

def get_db_connection():
    # Connection String
    connection_string = os.environ["ENV_DATABASE_CONNECTION_STRING"]
    
    return pyodbc.connect(connection_string)


def get_users(conn, r, req):
    #instantate pagination variables 
    count = req.params.get('count')
    if (not count):
        count = "10"
    page = req.params.get('page')
    if (not page):
        page = "1"
    
    USERS_CACHE_KEY = "users:" + "&count=" + count + "&page=" + page



    if (CACHE_TOGGLE == "On"): # check cache first
        try:
            cache = get_users_cache(r)
        except TypeError as e:
            logging.info(e.args[0])    

        if cache:
            logging.info("Returned data from cache")
            return func.HttpResponse(cache.decode('utf-8'), status_code=200, mimetype="application/json")
        else:         
            logging.info("Cache is empty, querying database...")


    #query database based on pagination variables
    start_index = (int(count) * int(page) - int(count))
    sql_query = "SELECT * FROM tasks ORDER BY taskId OFFSET " + str(start_index) + " ROWS FETCH NEXT " + str(count) + " ROWS ONLY"
        
           
    with conn.cursor() as cursor:
        logging.debug(
            "Using connection cursor to execute query (select " + count + " from users page " + page)
         
        try:
            cursor.execute(sql_query)
        except Exception as e:
            logging.info("Error: " + e.args[1])

        # Get users
        logging.debug("Fetching all queried information")
        users_table = list(cursor.fetchall())

        # Clean up to put them in JSON.
        users_data = [tuple(user) for user in users_table]

        # Empty data list
        users = []

        users_columns = [column[0] for column in cursor.description]
        for user in users_data:
            users.append(dict(zip(users_columns, user)))


        logging.debug(
            "User data retrieved and processed, returning information from get_users function")

        if (CACHE_TOGGLE == "On"): # Cache the results 
            cache_users(r, users)


        return func.HttpResponse(json.dumps(users, default=default), status_code=200, mimetype="application/json" )

        
def add_user(conn, user_req_body, r):
    # First we want to ensure that the request has all the necessary fields
    logging.debug("Testing the add new user request body for necessary fields...")
    try:
        assert "firstName" in user_req_body, "New user request body did not contain field: 'firstName'"
        assert "lastName" in user_req_body, "New user request body did not contain field: 'lastName'"
        assert "email" in user_req_body, "New user request body did not contain field: 'email'"
    except AssertionError as user_req_body_content_error:
        logging.critical("New user request body did not contain the necessary fields!")
        return func.HttpResponse(user_req_body_content_error.args[0], status_code=400)
    
    logging.debug("New user request body contains all the necessary fields!")
    with conn.cursor() as cursor:
        # Unpack user data
        firstName = user_req_body["firstName"]
        lastName = user_req_body["lastName"]
        email = user_req_body["email"]
        user_params = (firstName, lastName, email)

        # Create the query
        add_user_query = """
                         SET NOCOUNT ON;
                         DECLARE @NEWID TABLE(ID INT);
                         INSERT INTO dbo.users (firstName, lastName, email)
                         OUTPUT inserted.userId INTO @NEWID(ID)
                         VALUES(?, ?, ?);
                         SELECT ID FROM @NEWID
                         """

        logging.debug(
            "Using connection cursor to execute query (add a new user and get id)")
        
        count = cursor.execute(add_user_query, user_params)

        # Get the user id from cursor
        user_id = cursor.fetchval()

        clear_users_cache(r)
        
        logging.debug(
            "User added and new user id retrieved, returning information from add_user function")
        return func.HttpResponse(json.dumps({"userId": user_id}), status_code=200, mimetype="application/json")

# to handle datetime with JSON
# It serialize datetime by converting it into string
def default(dateHandle):
  if isinstance(dateHandle, (datetime.datetime, datetime.date)):
    return dateHandle.isoformat()

def init_redis():
    REDIS_HOST = os.environ['ENV_REDIS_HOST']
    REDIS_KEY = os.environ['ENV_REDIS_KEY']
    REDIS_PORT = os.environ['ENV_REDIS_PORT']

    return redis.StrictRedis(host=REDIS_HOST,
        port=REDIS_PORT, db=0, password=REDIS_KEY, ssl=True)

def cache_users(r, users):
    if (CACHE_TOGGLE == "On"):
        try: 
            logging.info("Caching results...")
            r.set(USERS_CACHE_KEY, json.dumps(users ,default=default), ex=1200)   
            logging.info("Caching complete")
        except Exception as e:
            logging.info("Caching failed")
            logging.info(e.args[0])

def get_users_cache(r):  
    if (CACHE_TOGGLE == "On"):
        logging.info("Querying cache...")
        try:
            cache = r.get(USERS_CACHE_KEY)
            return cache
        except Exception as e:
            logging.critical("Failed to fetch from cache: " + e.args[1])
            return None

def clear_users_cache(r):
    r.delete(USERS_CACHE_KEY)
    logging.info("Cache cleared")

def create_users_table(conn):
    cursor = conn.cursor()
    
    # First check to see if the table already exists
    tables = "tables: "
    for row in cursor.tables(tableType="TABLE"):
        tables += row.table_name
        tables += " "
    logging.debug(tables)

    if "users" not in tables:
        cursor.execute('''
            CREATE TABLE users (
                    userId INTEGER PRIMARY KEY IDENTITY,
                    firstName TEXT NOT NULL,
                    lastName  TEXT NOT NULL,
                    email TEXT NULL,            
            );
               ''')

    columns = "users columns: "
    for column in cursor.columns(table="users"):
        columns += column.column_name
        columns += " "
    logging.debug(columns)