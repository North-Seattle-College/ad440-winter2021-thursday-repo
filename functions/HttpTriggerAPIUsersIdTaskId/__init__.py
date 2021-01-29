"""This script runs the userId/taskId API endpoint functionality and consists of
    the main function, ODBC conenct function and 4 CRUD methods functions"""
import json
from datetime import datetime
import logging
import os
import pyodbc
import azure.functions as func

#GET API method function
def get(userId, taskId):
    #connects to db

    try:
        logging.debug('Attempting a db connection')
        cnxn = connect()
        cursor = cnxn.cursor() 
        logging.debug('opened connection')        
        logging.debug(f'Attempting to execute GET task query for task {taskId}')
        #Get task title, description and user name by userId and taskId
        sql_query = ("""SELECT tasks.userId, CONCAT (users.firstName, ' ', users.lastName) AS "user",
                    tasks.taskId, tasks.title, tasks.description, tasks.createdDate, tasks.dueDate, 
                    tasks.completed, tasks.completedDate 
                    FROM [dbo].[tasks] JOIN [dbo].[users] 
                    on [dbo].[tasks].userId = [dbo].[users].userId
                    WHERE [dbo].[users].userId = ? AND [dbo].[tasks].taskId = ?""")
        cursor.execute(sql_query, userId, taskId)
        logging.debug(f'Executed the GET query for {taskId}')          
        row = cursor.fetchone()
        logging.debug(f"Got result: {row}")
        if not row:
            logging.error('No record with the requested parameters')
            return func.HttpResponse('Task not found', status_code=404)
        else:
            columns = [column[0] for column in cursor.description]
            data = dict(zip(columns, row))
        return func.HttpResponse(json.dumps(data, default=str), status_code=200, mimetype="application/json")
    finally:
        cursor.close()
        cnxn.close()
        logging.debug('Closed the db connection')   

# #Parses JSON body received by the API
# def parse(task_req_body):
#        try:
#             #assert for the presense of appropriate fields in JSON
#             assert 'title' in task_req_body, "New task request body did not contain field: 'title'"
#             assert 'description' in task_req_body, "New task request body did not contain field: 'description'"
#             assert 'dueDate' in task_req_body, "New user request body did not contain field: 'dueDate'"
#             assert 'completed' in task_req_body, "New user request body did not contain field: 'completed'
#             assert 'completedDate' in task_req_body, "New user request body did not contain field: 'completedDate'"
#         except AssertionError as task_req_body_content_error:
#             logging.error('New user request body did not contain fields to update a task')
#             return func.HttpResponse(task_req_body_content_error.args[0], status_code=400)
#         logging.debug('New user request body contained necessary fields to update a task')  
#         # Unpack task data
#         title = task_req_body.get('title')
#         description = task_req_body.get('description')
#         dueDate = None
#         if task_req_body.get('dueDate') != None:
#             dueDate = datetime.strptime(task_req_body.get('dueDate'), '%d/%m/%y %H:%M:%S')  
#         completed = task_req_body.get('completed')
#         completedDate = datetime.strptime(task_req_body.get('completedDate'), '%d/%m/%y %H:%M:%S')      
#         # update task: title and description
#         sql_query = """UPDATE [dbo].[tasks]
#             SET title = ?, description = ?, dueDate = ?, completed = ?, completedDate = ?
#             WHERE userId = ? AND taskId = ?"""
#         try:
#             rowcount = cursor.execute(sql_query, title, description, dueDate, completed, completedDate, userId, taskId).rowcount
#             if not rowcount:
#                 logging.error('No record with the requested parameters exists in db')
#                 return func.HttpResponse('No record to update', status_code=404)                
#             logging.debug('UPDATE query executed')
#             logging.debug(f"Executed the query: {rowcount} rows affected for taskId {taskId}")
#             return func.HttpResponse(status_code=200)
#         except Exception as e:
#             logging.critical('Unable to execute the query')
#             return func.HttpResponse("Error: %s" % str(e), status_code=400)
#     finally:  

#PUT API method function
def update(userId, taskId, task_req_body):
    #connects to db
    cnxn = connect()
    cursor = cnxn.cursor()
    try:
        logging.debug('opened connection')        
        logging.debug(f'Going to execute UPDATE task {taskId} for user {userId} query')
        # task_req_body input check
        logging.debug("Checking the request body for necessary fields to update a task")
###HOW to ENSURE NOTHING IS WRONG WITH JSON (see code in main and move if reasonable)
###parse JSON in a separate file and validate there, pass the dictionary to this function
        try:
            #assert for the presense of appropriate fields in JSON
            assert 'title' in task_req_body, "New task request body did not contain field: 'title'"
            assert 'description' in task_req_body, "New task request body did not contain field: 'description'"
            assert 'dueDate' in task_req_body, "New user request body did not contain field: 'dueDate'"
            assert 'completed' in task_req_body, "New user request body did not contain field: 'completed'"
            assert 'completedDate' in task_req_body, "New user request body did not contain field: 'completedDate'"
        except AssertionError as task_req_body_content_error:
            logging.error('New user request body did not contain fields to update a task')
            return func.HttpResponse(task_req_body_content_error.args[0], status_code=400)
        logging.debug('New user request body contained necessary fields to update a task')  
        # Unpack task data
        title = task_req_body.get('title')
        description = task_req_body.get('description')
        dueDate = None
        if task_req_body.get('dueDate') != None:
            dueDate = datetime.strptime(task_req_body.get('dueDate'), '%d/%m/%y %H:%M:%S')  
        completed = task_req_body.get('completed')
        completedDate = None
        if task_req_body.get('completedDate') != None:
            completedDate = datetime.strptime(task_req_body.get('completedDate'), '%d/%m/%y %H:%M:%S')      
        # update task: title and description
        sql_query = """UPDATE [dbo].[tasks]
            SET title = ?, description = ?, dueDate = ?, completed = ?, completedDate = ?
            WHERE userId = ? AND taskId = ?"""
        try:
            rowcount = cursor.execute(sql_query, title, description, dueDate, completed, completedDate, userId, taskId).rowcount
            if not rowcount:
                logging.error('No record with the requested parameters exists in db')
                return func.HttpResponse('No record to update', status_code=404)                
            logging.debug('UPDATE query executed')
            logging.debug(f"Executed the query: {rowcount} rows affected for taskId {taskId}")
            return func.HttpResponse(status_code=200)
        except Exception as e:
            logging.critical('Unable to execute the query')
            return func.HttpResponse("Error: %s" % str(e), status_code=400)
    finally:
        #commits changes to db
        cnxn.commit()
        #properly closes the connection
        cursor.close()
        cnxn.close()
        logging.debug('Closed the db connection')    

#DELETE API method function
def delete(userId, taskId):
    #connects to db
    cnxn = connect()
    cursor = cnxn.cursor()
    try:
        logging.debug('opened connection')        
        logging.debug(f'Going to execute DELETE task {taskId} for user {userId} query')
        sql_query = ("""DELETE FROM [dbo].[tasks] WHERE userId = ? AND taskId = ?""")
        try:
            rowcount = cursor.execute(sql_query, userId, taskId).rowcount
            if not rowcount:
                logging.error('No record with the requested parameters exists in db')
                return func.HttpResponse('No record to delete', status_code=404)                
            logging.debug(f"Executed the DELETE query: {rowcount} rows affected for taskId {taskId}")
            return func.HttpResponse(status_code=200)
        except Exception as e:
            logging.error('Unable to execute the query')
            return func.HttpResponse("Error: %s" % str(e), status_code=400)
    finally:
        #commits changes to db
        cnxn.commit()
        #properly closes the connection
        cursor.close()
        cnxn.close()
        logging.debug('Closed the db connection')   

### POST API method function not implemented for this endpoint, use userId/tasks instead ### 

#connect to db function
def connect():
    try:
        #creates connection string
        db_server = os.environ["ENV_DATABASE_SERVER"]
        db_name = os.environ["ENV_DATABASE_NAME"]
        db_username = os.environ["ENV_DATABASE_USERNAME"]
        db_password = os.environ["ENV_DATABASE_PASSWORD"]
        driver = '{ODBC Driver 17 for SQL Server}'
        logging.debug('Uses hardcoded ODBC Driver 17 for SQL Server string')
        #assigns the connection string
        conn_string = "Driver={};Server={};Database={};Uid={};Pwd={};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;".format(
        driver, db_server, db_name, db_username, db_password)
     
        #creates and returns connection variable
        try:         
            logging.debug('Attempting DB connection')
            cnxn = pyodbc.connect(conn_string)
        except (pyodbc.InterfaceError) as e:
            logging.critical('Failed to connect to DB: ' + e.args[0])
        except (pyodbc.DatabaseError, pyodbc.InterfaceError) as e:
            logging.debug('Failed to connect to DB: ' + e.args[1])
            return func.HttpResponse(status_code=500)
        logging.debug("Connection to DB successful!")
        return cnxn
    except Exception as e:
        logging.error('Failure: ' + str(e))
        return func.HttpResponse(status_code=500)

#MAIN FUNCTION
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function started processing a userId taskId request.')

#collects parameters passed in url        
    userId = req.route_params.get('userId')
    taskId = req.route_params.get('taskId')
    logging.debug('Trying to get userId and taskId')
    req_body = {}
    try:
        req_body = req.get_json()
    except ValueError:
        pass
    if (not userId) and (not taskId):
        logging.debug("Got neither userId nor taskId")
        userId = req_body.get('userId')
        taskId = req_body.get('taskId')
    if userId and taskId: 
        logging.debug(f"Got userId:{userId} and taskId: {taskId}")

#determines which API method was requested, and calls the API method
    method = req.method

    try:
    #if GET method is selected, it executes here
        if method == "GET":  
            logging.debug('Passed GET method')      
            return (get(userId, taskId))

    #if PUT method is selected, it executes here
        elif method == "PUT":
            logging.debug('Passed PUT method')   
            return (update(userId, taskId, req_body))

    #if PATCH method is selected, it executes here
        elif method == "PATCH":
            logging.debug('Passed PATCH method')   
            return 

        elif method == "DELETE":
            logging.debug('Passed DELETE method')   
            return (delete(userId, taskId))
        else:
            logging.warn(f"Request with method {method} is not allowed for this endpoint")
            func.HttpResponse(status_code=405)

    #displays erros, if any, encountered when API methods were called
    except Exception as e:
        return func.HttpResponse("Error: %s" % str(e), status_code=500) 