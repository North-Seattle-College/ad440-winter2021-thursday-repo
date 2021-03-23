"""This script runs the userId/taskId API endpoint functionality and consists of
    the main function, ODBC conenct function and 4 CRUD methods functions"""
import json
from datetime import datetime
import logging
import os
import pyodbc
import azure.functions as func
import redis 

# Connect to the Redis Server
r = redis.StrictRedis(
    host= os.environ['ENV_REDIS_HOST'], 
    port=os.environ['ENV_REDIS_PORT'], 
    db=0,
    password= os.environ['ENV_REDIS_KEY'], 
    ssl=True)

# Global variables for Redis cache toggle and the invalidation of tasks all 
CACHE_TOGGLE = os.environ["CACHE_TOGGLE"],
USERS_USERID_TASKS_ALL_CACHE = b'users:{user_id}:tasks:all'
USERS_USERID_TASKS_TASKSID_CACHE= b'users:{user_id}/tasks/{task_id}'

#GET API method function
def get(userId, taskId, r):
    #connects to db

    try:
        logging.debug('Attempting a db connection')
        cnxn = connect()
        cursor = cnxn.cursor() 
        logging.debug('opened connection')        
        logging.debug(f'Attempting to execute GET task query for task {taskId}')

        try:
            # Implments method to check cahce for users
            cache = get_taskID_cache(r, userId, taskId)
           
        except TypeError as e:
            logging.info(e.args[0])

        if cache:
            logging.info("Returned data from cache")
            return func.HttpResponse(cache.decode('utf-8'), status_code=200, mimetype="application/json")

        else:
            #Get task title, description and user name by userId and taskId
            #Avoids using SELECT * to prevent retuning unwanted unformation
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
            
            # Cache the data in the GET  
            cache_users(r, data, userId, taskId)
            return func.HttpResponse(json.dumps(data, default=str), status_code=200, mimetype="application/json")

    finally:
        cursor.close()
        cnxn.close()
        logging.debug('Closed the db connection')   



#PUT API method function
def update(userId, taskId, task_fields):
    #connects to db
    try:
        cnxn = connect()
        cursor = cnxn.cursor()
        logging.debug('opened connection')        
        logging.debug(f'Going to execute UPDATE query task {taskId} for user {userId}') 
        try:
            # update task: with 5 required JSON fields
            assert len(task_fields) == 5, "Pass five required fields to update the task"
        except AssertionError as req_body_content_error:
            logging.error('Query did not contain all fields to update the task') 
            return func.HttpResponse(req_body_content_error.args[0], status_code=400)
        sql_query = """UPDATE [dbo].[tasks]
            SET title = ?, description = ?, dueDate = ?, completed = ?, completedDate = ?
            WHERE userId = ? AND taskId = ?"""   

        rowcount = cursor.execute(sql_query, task_fields.get('title'), task_fields.get('description'), 
        task_fields.get('dueDate'), task_fields.get('completed'), task_fields.get('completedDate'), 
        userId, taskId).rowcount
        if not rowcount:
            logging.error('Bad input and/or no record with the requested parameters exists in db')
            return func.HttpResponse('Bad or invalid input', status_code=404)                
        logging.debug('UPDATE task query executed')
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

#PATCH API method function, permits min 1 field passed in task_fields
def patch(userId, taskId, task_fields):
    #connects to db
    cnxn = connect()
    cursor = cnxn.cursor()
    logging.debug('opened connection')        
    logging.debug(f'Going to execute PATCH query on task {taskId} for user {userId}')  
    #creates a list of fields to update
    columnsToUpdate = list(task_fields.keys())
    #params list to later use in sql query
    params = []
    fieldsInQuery = ''
    #iterates through column values and adds them as params to be passed into sql query
    for column in columnsToUpdate:
        #accounts for no comma after the last param in the sql guery string
        if column == columnsToUpdate[-1]:
            comma = ' '
        else:
            comma = ', '
        #avoids potential sql injection by using ? placeholder for column values
        fieldsInQuery += "{} = ?{}".format(column, comma)
        #appends each of columns to the list
        params.append(task_fields.get(column))
    #adds userId and taskId to params
    params.extend([userId, taskId])
    #set the query body
    sql_query = """UPDATE [dbo].[tasks] SET {} WHERE userId = ? AND taskId = ?""".format(fieldsInQuery)
    try: 
        rowcount = cursor.execute(sql_query, params).rowcount
        #reports out an unsuccessful result
        if not rowcount:
            logging.error('Invalid input and/or no record with the requested parameters exists in db')
            return func.HttpResponse('Invalid input', status_code=404)                
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
def delete(userId, taskId,r):
    #connects to db
    cnxn = connect()
    cursor = cnxn.cursor()
    logging.debug('opened connection')        
    logging.debug(f'Going to execute DELETE query on task {taskId} for user {userId}')
    sql_query = ("""DELETE FROM [dbo].[tasks] WHERE userId = ? AND taskId = ?""")
    try:
        rowcount = cursor.execute(sql_query, userId, taskId).rowcount
        #returns error in the event of unsuccessful query
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
        # Connects to the 
        conn_string = os.environ["ENV_DATABASE_CONNECTION_STRING"]
     
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

# Parses the request body
def parse(req_body): 
    # sets up a dictionary to use in METHOD requests
    task_fields = {}
    logging.debug('''Parsing req_body into a dictionary. 
                Only title, description, completed, dueDate and completedDate may be updated''')
    #unpacks task data 
    #creates no dictionary entry if no corresponding field in req_body
    if req_body.get('completed'):
        #ensures "completed" value is not null
        try:
            assert req_body.get('completed') is not None, "Null value not permitted for the 'completed' field"
        except AssertionError as req_body_content_error:
            logging.error('Completed value may not be null') 
            return func.HttpResponse(req_body_content_error.args[0], status_code=400)
        #adds 'completed' to the dictionary
        task_fields['completed'] = req_body.get('completed')     
  
    if req_body.get('title'):
        task_fields['title'] = req_body.get('title')
 
    if req_body.get('description'):
        task_fields['description'] = req_body.get('description')
 
    dueDate = None
    #accounts for instances when the dueDate value passed is null, to avoid datetime conversion error
    if req_body.get('dueDate') is not None:
        dueDate = datetime.strptime(req_body.get('dueDate'), '%d/%m/%y %H:%M:%S')  
    task_fields['dueDate'] = dueDate
    
    completedDate = None
    #account for instances when the completedDate value passed is null, to avoid datetime conversion error
    if req_body.get('completedDate') is not None:
        completedDate = datetime.strptime(req_body.get('completedDate'), '%d/%m/%y %H:%M:%S')  
    task_fields['completedDate'] = completedDate

    #ensures there is at least one value passed from req_body to the dictionary / dict not empty
    try:
        assert bool(task_fields), "JSON Body must contain at least one task field"
    #raises error when the dictionary is empty
    except AssertionError as req_body_content_error:
        logging.error('New user request body did not contain fields to update the task')
        return func.HttpResponse(req_body_content_error.args[0], status_code=400)
    logging.debug(f'Request body contained one or more fields to update the task: {task_fields}')  
    return task_fields 

#MAIN FUNCTION
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function started processing a userId taskId request.')

    #collects userId and taskId parameters passed in url        
    logging.debug('Trying to get userId and taskId')
    userId = req.route_params.get('userId')
    taskId = req.route_params.get('taskId')
    if userId and taskId: 
        logging.debug(f"Got userId:{userId} and taskId: {taskId}")
    if (not userId) and (not taskId):
        logging.debug("Did not receive userId and/or taskId")
        return func.HttpResponse('Endpoint requires userId and taskId', status_code=400)
    #determines which API method was requested, and calls the API method
    method = req.method
    try:
    #if GET method is selected, it executes here
        if method == "GET":  
            logging.debug('Passed GET method')  
            # ADDED implementation of redis r=redis    
            return (get(userId, taskId,r))

    #if DELETE method is selected, it executes here
        if method == "DELETE":
            logging.debug('Passed DELETE method')  
            
            # Invalidate users tasks all call 
            invalidate_users_tasks_all_cache(r)
            
            # ADDED implementation of redis r=redis 
            return (delete(userId, taskId,r))

        #examines JSON passed by the client, required for PUT and PATCH execution
        req_body = {}
        try:
            req_body = req.get_json()
        #passes error if not
        except ValueError:
            logging.error('Empty req body or non-JSON file passed')
            pass
        task_fields = parse(req_body)

        #if PUT method is selected, it executes here 
        if method == "PUT":
            logging.debug('Passed PUT method')  
            
            # Invalidate users tasks all call 
            invalidate_users_tasks_all_cache(r) 
            
            # ADDED implementation of redis r=redis
            return (update(userId, taskId, task_fields,r))

        #if PATCH method is selected, it executes here
        elif method == "PATCH":
            logging.debug('Passed PATCH method')   
            return (patch(userId, taskId, task_fields))
        else:
            logging.warn(f"Request with method {method} is not allowed for this endpoint")
            func.HttpResponse(status_code=405)

    #displays other erros, if any, encountered when API methods were called
    except Exception as e:
        return func.HttpResponse("Error: %s" % str(e), status_code=500) 

# method to check if the request is already in the cache
def get_taskID_cache(r, userId, taskId):
    logging.info("Querying cache...")
    key = "users:" + userId + ":tasks:" + taskId
    # CACHE TOGGLE to turn off and on the cache for developers
    if(CACHE_TOGGLE):
        try:
            cache = r.get(key)
            return cache
        except TypeError as e:
            logging.critical("Failed to fetch from cache: " + e.args[1])
            return None
# Method to cache the users and tasks
def cache_users(r, task, userId, taskId):
    key = "users:" + userId + ":tasks:" + taskId
    # CACHE TOGGLE to turn off and on the cache for developers
    if(CACHE_TOGGLE):
        try: 
            r.set(key, json.dumps(task, default=str), ex=1200)   
            logging.info("Caching complete")
        except TypeError as e:
            logging.info("Caching failed")
            logging.info(e.args[0])

# Invalidate users tasks all method
def invalidate_users_tasks_all_cache(r):
    r.delete(USERS_USERID_TASKS_ALL_CACHE)
    logging.info("Cache Invalidated")

