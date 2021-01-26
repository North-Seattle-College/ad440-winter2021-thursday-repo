import logging
import os
import pyodbc
import azure.functions as func

#GET API method function
def get(param1, param2):
    #connects to db
    cnxn = connect()
    cursor = cnxn.cursor()
    logging.info('opened connection')        
    logging.info('Going to execute select query')
    try:
        #Get task title, description and user name by userId and taskId
        sql_query = ("""SELECT tasks.title, tasks.description, CONCAT (users.firstName, ' ', users.lastName) AS "user" 
        FROM [dbo].[tasks] JOIN [dbo].[users] 
        on [dbo].[tasks].userId = [dbo].[users].userId
        WHERE [dbo].[users].userId = ? AND [dbo].[tasks].taskId = ?""")
        cursor.execute(sql_query, param1, param2)
        logging.info('Executed the query')         
        data = cursor.fetchall()
        logging.info(f"Got result: {data}")
        return data
#irrespective of results, closes connection
    finally:
        cursor.close()
        cnxn.close()
        logging.info('Closed the connection')

#POST API method function       
def post(param):
    return ('You selected POST method with {param} values. Functionality under construction')
            # STARTER CODE FOR NEXT SPRINT, SQL QUERY TESTED
            #     #insert row into tasks table / create a new task
            #     #createdDate #'20120618 10:34:09 AM' and title/description are hardcoded for sprint1, update with automated date stamp and url params later
            #     sql_query = ("""INSERT INTO dbo.tasks (userId, title, description, createdDate)
            #     VALUES (?, ?, ?, '20120618 10:34:09 AM')""")
            #     cursor.execute(sql_query, userId, 'Do It', 'Almost like Nike motto')   
            #     logging.info('Executed the query')

#UPDATE API method function
def update(param1, param2):
    #connects to db
    cnxn = connect()
    cursor = cnxn.cursor()
    logging.info('opened connection')        
    logging.info('Going to execute update query')
    try:
        # update task: title and description. Client passes userId and taskId, 
        # for sprint 1 other fields are HARDCODED
        sql_query = ("""UPDATE [dbo].[tasks]
        SET title = 'Title updated by team1', description = 'Description updated by team1'
        WHERE userId = ? AND taskId = ?""")   
        rowcount = cursor.execute(sql_query, param1, param2).rowcount
        logging.info(f"Executed the query: {rowcount} rows affected")
#commits changes to db
        cnxn.commit()
        return rowcount
#irrespective of results, closes connection
    finally: 
        cursor.close()
        cnxn.close()
        logging.info('Closed the connection')

#DELETE API method function
def delete(param):
    return ('You selected POST method with {param} values. Functionality under construction')
            # STARTER CODE FOR NEXT SPRINT, SQL QUERY TESTED
            #     # #delete row, client passes in userId and taskId
            #     sql_query = ("""DELETE FROM [dbo].[tasks] WHERE userId = ? AND taskId = ?""")
            #     cursor.execute(sql_query, userId, taskId)
            #     logging.info('Executed the query')
            #     cnxn.commit()

#connect to db function
def connect():
    try:
        #creates connection string
        db_server = os.environ["ENV_DATABASE_SERVER"]
        db_name = os.environ["ENV_DATABASE_NAME"]
        db_username = os.environ["ENV_DATABASE_USERNAME"]
        db_password = os.environ["ENV_DATABASE_PASSWORD"]
        driver = '{ODBC Driver 17 for SQL Server}'
        conn_string = "Driver={};Server={};Database={};Uid={};Pwd={};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;".format(
        driver, db_server, db_name, db_username, db_password)

# when passwords are permitted be saved to the config of the Azure function app, 
# using a single connection string value, saved to the config of the app, 
# is more economical : <conn_string = os.getenv('SQL_CONNECTION_STRING')>, get the string
# from "Connection strings" menu on the left, in the database of interest        
        #creates and returns connection variable
        cnxn = pyodbc.connect(conn_string)
        return cnxn
    except Exception:
        print ("Unable to connect to db. Code 503: Service unavailable")

#MAIN FUNCTION
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

#collects parameters passed in url        
    userId = req.params.get('userId')
    taskId = req.params.get('taskId')
    logging.info('Trying to get userId and taskId')
    if (not userId) and (not taskId):
        logging.info("Got neither userId nor taskId")
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            userId = req_body.get('userId')
            taskId = req_body.get('taskId')
    if userId and taskId: 
        logging.info(f"Got userId:{userId} and taskId: {taskId}")

#determines which API method was requested, and calls the API method
    method = req.method
    if not method:
        logging.critical('No method available')
        raise Exception('No method passed')

    try:
    #if GET method is selected, it executes here
        if method == "GET":        
            getResult = get(userId, taskId)
            return func.HttpResponse(f"This {method} method was called. You entered {userId} as userId and {taskId} as taskId. Result: {getResult}")

    #if POST method is selected, it executes here
        if method == "POST":
            postResult = post(method)
            return func.HttpResponse(f"Temp results: {postResult}")

    #if UPDATE method is selected, it executes here
        if method == "UPDATE":
            updateResult = update(userId, taskId)
            return func.HttpResponse(f"This {method} method was called. You entered {userId} as userId and {taskId} as taskId. Result: {updateResult}")

    #if DELETE method is selected, it executes here
        if method == "DELETE":
            deleteResult = delete(method)
            return func.HttpResponse(f"Temp results: {deleteResult}") 
    #displays erros encountered when API methods were called
    except Exception as e:
        return func.HttpResponse("Error: %s" % str(e), status_code=500) 
    #prompts clients to pass url parameters
    else:
        logging.info('Got only one of userId and taskId')
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a method, userId and taskId for an appropriate response.",
            status_code=200
        ) 
    logging.info('Finishing the function without error')
    return func.HttpResponse("Nothing done")