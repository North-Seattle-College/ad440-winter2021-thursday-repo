import logging
import pyodbc
import os
import azure.functions as func
import json
import redis

# This is the Http Trigger for Users/userId
# It connects to the db and retrives the users added to the db by userId

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(
        'Python HTTP trigger for users/userId is processing a request ')

    #Initiating REDIS cache
    REDIS_HOST = 'nsc-redis-dev-usw2-thursday.redis.cache.windows.net'
    r = redis.Redis(host= REDIS_HOST, port= 6380, db= 0, password= os.environ["ENV_REDIS_KEY"], ssl= True)

    #Something to test the redis cache
    r.get("2")

    # Database credentials.
    db_server = os.environ["ENV_DATABASE_SERVER"]
    db_name = os.environ["ENV_DATABASE_NAME"]
    db_username = os.environ["ENV_DATABASE_USERNAME"]
    db_password = os.environ["ENV_DATABASE_PASSWORD"]
    driver = '{ODBC Driver 17 for SQL Server}'
    connectionString = "Driver={};Server={};Database={};Uid={};Pwd={};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;".format(
        driver, db_server, db_name, db_username, db_password)


    try:
        # Create a new connection
        logging.debug("Attempting DB connection!")
        with pyodbc.connect(connectionString) as conn:
            with conn.cursor() as cursor:
                logging.debug("Connection to DB successful!")

                # Get user id from url (...api/users/{user_id}) and query db to check if it exists
                user_id = req.route_params.get('userId')
                logging.debug("Check if userId exists in database: " + user_id)
                row = get_user_row(cursor, user_id)
                if not row:
                    logging.debug("User Id not found")
                    return func.HttpResponse(
                        "User not found",
                        status_code=404
                    )
                if req.method == 'GET':
                    return get(cursor, row, r)
                elif req.method == 'PUT':
                    return put(req, cursor, user_id)
                elif req.method == 'DELETE':
                    return delete(cursor, user_id)
                else:
                    return methodNotAllowed()

    except Exception as e:
        logging.critical("Error: %s" % str(e))
        return func.HttpResponse(
            "Internal Server Error",
            status_code=500
        )

#This method calls the retrieves the user based on user_id and caches the user info on Redis
def get(cursor, row, r):
    logging.debug("Attempting to retrieve user by ID...")
    # This will convert the results from the query into json properties.
    # More information can be found on the link below:
    # https://stackoverflow.com/questions/16519385/output-pyodbc-cursor-results-as-python-dictionary/16523148#16523148
    try:
        cache = get_user_id_cache(r, userId)
    except TypeError as e:
        logging.info(e.args[0])
    if cache:
        logging.info("Data returned from cache")
        return func.HttpResponse(cache.decode('utf-8'), status_code =200, mimetype="application/json")
    else:
        logging.info("Empty cache, querying...")
        sql_query = ("""SELECT CONCAT (users.firstName, ' ', users.lastName) AS "user",
                        FROM [dbo].[users] 
                        WHERE [dbo].[users].userId = ?""")
        cursor.execute(sql_query, userId)

    #gets user(s)
    logging.debug("Fetching all queries for User IDs")
    user_id_table = list(cursor.fetchall())

    #Cleans User ID data to put into table
    user_id_data = [tuple(user_id) for user_id in user_id_table]

    #Empty User ID list
    user_id_list = []

    #Add data to empty list
    user_id_columns = [column[0] for column in cursor.description]
    for user_id in user_id_data:
        user_id_list.append(dict(zip(columns, row))) 

    logging.debug("Users retrieved successfully!")

    #Caches the User ID data
    cache_user_id(r, user_id)

    return func.HttpResponse(
        json.dumps(data),
        status_code=200,
        mimetype="application/json"
    )


# For POST and PATCH
def methodNotAllowed():
    logging.debug("This method is not Implemented")
    return func.HttpResponse(
        "Method not allowed!",
        status_code=405
    )


def put(req, cursor, user_id):
    user_req_body = req.get_json()

    # Validate request body
    logging.debug("Verifying fields in request body to update a user by ID")
    try:
        assert "firstName" in user_req_body, "User request body did not contain field: 'firstName'"
        assert "lastName" in user_req_body, "User request body did not contain field: 'lastName'"
        assert "email" in user_req_body, "User request body did not contain field: 'email'"
    except AssertionError as user_req_body_content_error:
        logging.error(
            "User request body did not contain the necessary fields!")
        return func.HttpResponse(user_req_body_content_error.args[0], status_code=400)
    logging.debug("User request body contains all the necessary fields!")

    # Unpack user data
    firstName = user_req_body["firstName"]
    lastName = user_req_body["lastName"]
    email = user_req_body["email"]

    # Update user in DB
    update_user_query = "UPDATE dbo.users SET firstName = ?, lastName = ?, email = ? WHERE userId= ?"
    logging.debug("Executing query: " + update_user_query)
    cursor.execute(update_user_query,
                   (firstName, lastName, email, user_id))
    logging.debug("User was updated successfully!.")
    return func.HttpResponse(
        "User updated",
        status_code=200
    )


def delete(cursor, user_id):
    logging.debug("Attempting to retrieve user by ID and delete the user...")
    delete_user_query = "DELETE FROM dbo.users  WHERE userId= ?"
    logging.debug("Executing query: " + delete_user_query)
    cursor.execute(delete_user_query, (user_id,))
    logging.debug("User was deleted successfully!.")
    return func.HttpResponse(
        "User deleted",
        status_code=200
    )


def get_user_row(cursor, user_id):
    cursor.execute(
        "SELECT * FROM dbo.users WHERE userId= ?", (user_id,))

    return cursor.fetchone()

#This method caches user_id
#param: r- redis cache
#user_id: User IDs that need to cached
def cache_user_id(r, user_id):
    key = "users:" + userId
    try:
        r.set(key, json.dumps(users), ex= 1200) 
        logging.info("Caching complete!")
    except TypeError as e:
        logging.info("Caching failed")
        logging.info(e.args[0])

#This method retrieves the user_id cache
#param: r- Redis Cache that it the user_id cache residing in
def get_user_id_cache(r, userId):
    logging.info("Querying for User ID cache...")
    try:
        key = "users:" + userId
        cache = r.get(key)
        return cache
    except TypeError as e:
        logging.critical("Failed to fetch from cache: " + e.args[1])
        return None