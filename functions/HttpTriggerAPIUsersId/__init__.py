import logging
import pypyodbc
import os
import azure.functions as func
import json

# This is the Http Trigger for Users/userId
# It connects to the db and retrives the users added to the db by userId


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(
        'Python HTTP trigger for users/userId is processing a request ')

    # Database credentials.
    db_server = os.environ["ENV_DATABASE_SERVER"]
    db_name = os.environ["ENV_DATABASE_NAME"]
    db_username = os.environ["ENV_DATABASE_USERNAME"]
    db_password = os.environ["ENV_DATABASE_PASSWORD"]
    driver = '{ODBC Driver 17 for SQL Server}'
    connectionString = "Driver={};Server={};Database={};Uid={};Pwd={};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;".format(
        driver, db_server, db_name, db_username, db_password)

    # This gets the userId from the query string
    user_id = req.route_params.get('userId')
    try:
        # Create a new connection
        logging.debug("Attempting DB connection!")
        with pypyodbc.connect(connectionString) as conn:
            logging.debug("Connection to DB successful!")

            if req.method == 'GET':
                return get(conn, user_id)
            elif req.method == 'POST':
                return post()
            elif req.method == 'PUT':
                return put(req, conn, user_id)
            elif req.method == 'PATCH':
                return patch()
            elif req.method == 'DELETE':
                return delete(conn, user_id)

            conn.close()
            logging.debug('Connection to DB closed')

    except Exception as e:
        logging.critical("Error: %s" % str(e))
        return func.HttpResponse(
            "Internal Server Error",
            status_code=500
        )


def get(conn, user_id):
    logging.debug("Attempting to retrieve user by ID...")
    query_params = (user_id,)
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM users WHERE userId= ?", query_params)
        row = cursor.fetchone()
        if not row:
            logging.debug("User Id not found")
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

            logging.debug("Users retrieved successfully!")
            return func.HttpResponse(
                json.dumps(data),
                status_code=200,
                mimetype="application/json"
            )


def post():
    logging.debug("POST is not implemented")
    return func.HttpResponse(
        "Method not allowed!",
        status_code=405
    )


def put(req, conn, user_id):
    user_req_body = req.get_json()
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
    with conn.cursor() as cursor:
        # Unpack user data
        firstName = user_req_body["firstName"]
        lastName = user_req_body["lastName"]
        email = user_req_body["email"]
        query_params1 = (user_id,)
        query_params2 = (firstName, lastName, email, user_id)

        try:
            logging.debug("Check if userId exists: " + user_id)
            cursor.execute(
                "SELECT * FROM users WHERE userId= ?", query_params1)
            row = cursor.fetchone()
            if not row:
                return func.HttpResponse(
                    "User not found",
                    status_code=404
                )

            # Update user  query
            update_user_query = "UPDATE dbo.users SET firstName = ?, lastName = ?, email = ? WHERE userId= ?"
            logging.debug("Executing query: " + update_user_query)
            cursor.execute(update_user_query, query_params2)
            logging.debug("User was updated successfully!.")
            return func.HttpResponse(
                "User updated",
                status_code=200
            )
        except Exception as e:
            logging.critical("Error: " + e.args[1])
            return func.HttpResponse(
                "Internal Server Error",
                status_code=500
            )


def patch():
    logging.debug("PATCH is not implemented")
    return func.HttpResponse(
        "Method not allowed!",
        status_code=405
    )


def delete(conn, user_id):
    logging.debug("Attempting to retrieve user by ID and delete the user...")
    with conn.cursor() as cursor:
        query_params = (user_id,)
        try:
            logging.debug("Check if userId exists in database: " + user_id)
            cursor.execute(
                "SELECT * FROM users WHERE userId= ?", query_params)
            row = cursor.fetchone()
            if not row:
                return func.HttpResponse(
                    "User not found",
                    status_code=404
                )
            delete_user_query = "DELETE FROM dbo.users  WHERE userId= ?"
            logging.debug("Executing query: " + delete_user_query)
            cursor.execute(delete_user_query, query_params)
            logging.debug("User was deleted successfully!.")
            return func.HttpResponse(
                "User deleted",
                status_code=200
            )
        except Exception as e:
            logging.critical("Error: " + e.args[1])
            return func.HttpResponse(
                "Internal Server Error",
                status_code=500
            )
