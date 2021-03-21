import json
from datetime import datetime
import logging
import os
import pymysql

logging.getLogger().setLevel(logging.DEBUG)

# Lambda Handler parameters:
# event is a JSON-formatted document that contains data for a Lambda function to process
# context provides info about invocation, function, and runtime environment 

def lambda_handler(event, context):
    logging.info("Python function started processing a userId taskId request.")
    logging.info(event)

    method = event["requestContext"]["http"]["method"]
        
    logging.debug(f"{method} called")
    userId = event["pathParameters"]["userId"]
    taskId = event["pathParameters"]["taskId"]
    if userId and taskId: 
        logging.debug(f"Received {userId} and {taskId} as parameters")
    if (not userId) and (not taskId):
        logging.debug("Did not receive userId and/or taskId")
        logging.error("Error: bad userId and/or taskId parameters")
        return {
            "statusCode": 500
        }
    conn = connect()     
    try:
    #if GET method is selected, it executes here
        if method == "GET":  
            logging.debug("Passed GET method")      
            return get(userId, taskId, conn)

    #if DELETE method is selected, it executes here
        if method == "DELETE":
            logging.debug("Passed DELETE method")   
            return delete(userId, taskId, conn)

        #examines JSON passed by the client, required for PUT and PATCH execution
        req_body = {}
        try:
            req_body = json.loads(event["body"])
        #passes error if not
        except ValueError:
            logging.error("Empty req body or non-JSON file passed")
            pass
        task_fields = parse(req_body)

        #if PUT method is selected, it executes here
        if method == "PUT":
            logging.debug("Passed PUT method")   
            return update(userId, taskId, task_fields, conn)

        #if PATCH method is selected, it executes here
        elif method == "PATCH":
            logging.debug("Passed PATCH method")   
            return patch(userId, taskId, task_fields, conn)
        else:
            logging.warn(f"Request with method {method} is not allowed for this endpoint")
            return {
                "statusCode": 405
            }
    #displays other errors, if any, encountered when API methods were called
    except Exception as e:
        logging.error(f"Error: {str(e)}"),
        return {
            "statusCode": 500
        }
        
#connect to db function
def connect():
    try:         
        logging.debug("Attempting DB connection")
        cnxn = pymysql.connect(
        #creates connection string
        host            = os.environ["rds_hostname"],
        user            = os.environ["rds_username"],
        password        = os.environ["rds_password"],
        database        = os.environ["rds_db_name"],
        connect_timeout = 5
        )
    except pymysql.MySQLError as e:
        logging.critical(f"Failed to connect to DB: {e}, errno is {e.args[0]}")
        return {
            "statusCode": 500
        }
    logging.debug("Connection to DB successful!")
    return cnxn

# Parses the request body
def parse(req_body): 
    # sets up a dictionary to use in METHOD requests
    task_fields = {}
    logging.debug("""Parsing req_body into a dictionary. 
                Only title, description, completed, dueDate and completedDate may be updated""")
    #unpacks task data 
    #creates no dictionary entry if no corresponding field in req_body
    if req_body.get("completed"):
        #ensures "completed" value is not null
        try:
            assert req_body.get("completed") is not None, "Null value not permitted for the 'completed' field"
        except AssertionError as e:
            logging.error("Completed value may not be null") 
            return {
                "error": str(e),
                "statusCode": 400
            } 
        #adds "completed" to the dictionary
        task_fields["completed"] = req_body.get("completed")     
  
    if req_body.get("title"):
        task_fields["title"] = req_body.get("title")
 
    if req_body.get("description"):
        task_fields["description"] = req_body.get("description")
 
    # #accounts for instances when the dueDate value passed is null, converts datetime otherwise
    # if not req_body.get("dueDate"): 
    #     pass
    if req_body.get("dueDate") is not None:
        dueDate = datetime.strptime(req_body.get("dueDate"), "%d/%m/%y %H:%M:%S")  
        task_fields["dueDate"] = dueDate
    
    # #accounts for instances when the dueDate value passed is null, converts datetime otherwise
    # if not req_body.get("completedDate"): 
    #     pass 
    if req_body.get("completedDate") is not None:
        completedDate = datetime.strptime(req_body.get("completedDate"), "%d/%m/%y %H:%M:%S")  
        task_fields["completedDate"] = completedDate

    #ensures there is at least one value passed from req_body to the dictionary / dict not empty
    try:
        assert bool(task_fields), "JSON Body must contain at least one task field"
    #raises error when the dictionary is empty
    except AssertionError as e:
        logging.error("New user request body did not contain fields to update the task")
        logging.critical("Unable to execute the query")
        return {
            "error": str(e),
            "statusCode": 400
        } 
    logging.debug(f"Request body contained one or more fields to update the task: {task_fields}")  
    return task_fields 

#GET API method function
def get(userId, taskId, conn):      
    logging.info(f"Attempting to execute GET task query for task {taskId}")
    #Gets task info by userId and taskId
    #Avoids using SELECT * to prevent retuning unwanted information

    sql_query = ("""SELECT tasks.userId, CONCAT (users.firstName, ' ', users.lastName) AS "user",
    tasks.taskId, tasks.title, tasks.description, tasks.createdDate, tasks.dueDate, 
    tasks.completed, tasks.completedDate 
    FROM tasks JOIN users
    on tasks.userId = users.userId
    WHERE users.userId = %s AND tasks.taskId = %s""")
    try:
        with conn.cursor() as cursor: #opens a temp cursor that is closed with indentation return
            logging.info("opened a temp cursor")
            cursor.execute(sql_query, (userId, taskId))
            logging.debug(f"Executed the GET query for {taskId}")          
            row = cursor.fetchone()
            logging.debug(f"Got result: {row}")
            if not row:
                logging.error("No record with the requested parameters")
                logging.critical("Unable to execute the query")
                response = "Task not found"
                statusCode = 404
            else:
                columns = [column[0] for column in cursor.description]
                logging.info("collected columns")
                data = dict(zip(columns, row))
                logging.debug("parsed to dict")
                return json.dumps(data, default=str)
        #properly closes the connection
        conn.close()
        logging.debug("Closed the db connection")   
    except Exception as e:
        response = "GET failed"
        logging.critical(response)
        logging.error(e.args[0])
        statusCode = 400
    return {
        "statusCode": statusCode,
        "body":response,
        "headers": {"Content-Type":"application/json"}
    }
    
#PUT API method function
def update(userId, taskId, task_fields, conn):
    logging.info(f"Going to execute UPDATE query task {taskId} for user {userId}") 
    length = len(task_fields)
    logging.info(f"dictionary length is {length}") 
    # check for 5 required fields:
    try:
        assert length == 5, "Pass five required fields to update the task"
        sql_query = """UPDATE tasks
            SET title = %s, description = %s, dueDate = %s, completed = %s, completedDate = %s
            WHERE userId = %s AND taskId = %s"""  
        params = [task_fields.get("title"), task_fields.get("description"), task_fields.get("dueDate"),
            task_fields.get("completed"), task_fields.get("completedDate"), userId, taskId]
        logging.info("set the params")
        with conn.cursor() as cursor: 
            logging.info("Initiated the cursor")
            rows = cursor.execute(sql_query, params)
            conn.commit()         
            logging.debug("PUT task query executed")
            #properly closes the connection
            conn.close()
            logging.debug("Closed the db connection")  
            return {
                "body": f"PUT task query: {rows} rows affected for taskId {taskId}"
            }
    except AssertionError as e:
        logging.error(e.args[0])
        statusCode = 400 
        return {
            "statusCode": 400,
            "body":"PUT failed",
            "headers": {"Content-Type":"application/json"}
        }
        
#PATCH API method function, permits min 1 field passed in task_fields
def patch(userId, taskId, task_fields, conn): 
    #connects to db
    logging.debug("opened connection")        
    logging.info(f"Going to execute PATCH query on task {taskId} for user {userId}")  
    #creates a list of fields to update
    columnsToUpdate = list(task_fields.keys())
    #params list to later use in sql query
    params = []
    fieldsInQuery = ""
    #iterates through column values and adds them as params to be passed into sql query
    for column in columnsToUpdate:
        #accounts for no comma after the last param in the sql query string
        if column == columnsToUpdate[-1]:
            comma = " "
        else:
            comma = ", "
        #avoids potential sql injection by using ? placeholder for column values
        fieldsInQuery += "{} = %s{}".format(column, comma)
        #appends each of columns to the list
        params.append(task_fields.get(column))
    logging.debug(fieldsInQuery)
    #adds userId and taskId to params
    params.extend([userId, taskId])
    #set the query body
    sql_query = """UPDATE tasks SET {} WHERE userId = %s AND taskId = %s""".format(fieldsInQuery)
    logging.debug(sql_query)
    try: 
        with conn.cursor() as cursor: #opens a temp cursor that is closed with indentation return
            logging.debug("Initiated the cursor")
            rows = cursor.execute(sql_query, params)
            conn.commit()         
            logging.debug("PATCH task query executed")
            return {
                "body": f"Executed the query: {rows} rows affected for taskId {taskId}"
            }
            #properly closes the connection        
            conn.close()
            logging.debug("Closed the db connection")  
    except Exception as e:
        logging.error(e.args[0])
        return {
            "statusCode": 500,
            "body":"PATCH failed",
            "headers": {"Content-Type":"application/json"}
        }

#DELETE API method function
def delete(userId, taskId, conn):       
    logging.info(f"Going to execute DELETE query on task {taskId} for user {userId}")
    sql_query = ("""DELETE FROM tasks WHERE userId = %s AND taskId = %s""")
    try:    
        with conn.cursor() as cursor: #opens a temp cursor that is closed with indentation return
            logging.debug("Initiated the cursor")
            logging.debug(sql_query)
            row = cursor.execute(sql_query, (userId, taskId))
            if not row:
                conn.close()
                logging.debug("Closed the db connection")  
                return {
                    "body": "Invalid input",
                    "statusCode": 404
                }
            logging.info(f"Executed the DELETE query for {taskId}")          
            #returns error in the event of unsuccessful query
            conn.commit()         
            logging.debug("Delete task query executed and committed")
            #properly closes the connection
            conn.close()
            logging.debug("Closed the db connection")  
            return {
                "body": f"DELETE task query: {row} rows affected for taskId {taskId}"
            }
    except Exception as e:
        logging.error(e.args[0])
        return {
            "statusCode": 500,
            "body":"DELETE failed",
            "headers": {"Content-Type":"application/json"}
        }