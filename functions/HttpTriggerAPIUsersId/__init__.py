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
    # TODO  error handleing like lenny

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

                if req.method == 'GET':
                    return get(req, conn, id)
                elif req.method == 'POST':
                    return post(req, conn, id)
                elif req.method == 'PUT':
                    return put(req, conn, id)
                elif req.method == 'PATCH':
                    return patch(req, conn, id)
                elif req.method == 'DELETE':
                    return delete(req, conn, id)

                # Close connection after method call
                conn.close()
                logging.info('Closed the connection')

        except pypyodbc.DatabaseError as e:
            # 28000 - This code is returned by pypyodbc meaning Unautroized when a bad password is supplied etc
            # 42000 - Azure firewall blocks ip
            # Adddtional error handeling will need to be implemented, maybe in srpint 2

            # TODO ADD LOGGING with error detail
            if e.args[0] == '28000' or e.args[0] == '42000':
                return func.HttpResponse(
                    "Unauthorized",
                    status_code=403
                )
        else:
            return func.HttpResponse(
                "Error",
                status_code=400
            )


def get(req, conn, id):
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
            cursor.close()

            return func.HttpResponse(
                json.dumps(data),
                status_code=200,
                mimetype="application/json"
            )


def post(req, conn, id):
    return func.HttpResponse(
        "Method not allowed!",
        status_code=405
    )


def put(req, conn, id):
    user_req_body = req.get_json()
    try:
        assert "firstName" in user_req_body, "New user request body did not contain field: 'firstName'"
        assert "lastName" in user_req_body, "New user request body did not contain field: 'lastName'"
        assert "email" in user_req_body, "New user request body did not contain field: 'email'"
    except AssertionError as user_req_body_content_error:
        logging.error(
            "New user request body did not contain the necessary fields!")
        return func.HttpResponse(user_req_body_content_error.args[0], status_code=400)

    with conn.cursor() as cursor:
        # Unpack user data
        firstName = user_req_body["firstName"]
        lastName = user_req_body["lastName"]
        email = user_req_body["email"]
        user_params = (firstName, lastName, email)

        # Update user  query
        update_user_query = "UPDATE users SET firstName = {}, lastName = {}, email = {} WHERE userId={}".format(
            firstName, lastName, email, id)

        cursor.execute(update_user_query)


def patch(req, conn, id):
    return func.HttpResponse(
        "Method not allowed!",
        status_code=405
    )


def delete(req, conn, id):
    return ""
# Implement Response codes:
#  responses:
#         "200":
#           description: "User Deleted Successfully"
#         "400":
#           description: "Bad Request"
#         "401":
#           description: "Unauthorized"
#         "403":
#           description: "Forbidden"
#         "404":
#           description: "User Not Found"
#         "429":
#           description: "Too Many Requests"
#         "500":
#           description: "Internal Server Error"
#         "502":
#           description: "Bad Gateway"
#         "503":
#           description: "Service Unavailable"
