import json
import pyodbc
import logging
import os
import azure.functions as func
import datetime
import redis 



redisFeature = 'true';

# to handle datetime with JSON
# It serialize datetime by converting it into string
def default(dateHandle):
  if isinstance(dateHandle, (datetime.datetime, datetime.date)):
    return dateHandle.isoformat()

# to handle datetime with JSON
# It serialize datetime by converting it into string
def default(o):
  if isinstance(o, (datetime.datetime, datetime.date)):
    return o.isoformat()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(
        'Python HTTP trigger for /users/userId endpoint.')

    method = req.method
    user_id = req.route_params.get('userId')

    



    try:
        conn = connect_to_db()
    except (pyodbc.DatabaseError, pyodbc.InterfaceError) as e:
        logging.critical("connection failed: " + e.args[0])
        logging.debug("Error: " + e.args[1])
        return func.HttpResponse(status_code=500)
    logging.debug("Connected to DB successfuly!")

    #Redis Sever

    if(redisFeature):
        try:
            rDBpassword = os.enviorn["ENV_REDIS_KEY"]
            rDBhost = os.environ["ENV_REDIS_HOST"]
            rDBport = os.environ["ENV_REDIS_PORT"]
            rDB = redis.Redis(host=rDBhost, port=rDBport, db=0, password=rDBpassword, ssl=True) 
            rDB.ping()
            logging.debug("Connected to Redis!")
        except(redis.exceptions.ConnectionError, ConnectionRefusedError) as e:
                logging.error("Redis connection error!" + e.args[0])
    
    try:
        if method == "GET":
            logging.debug("trying to get one user with id {} all tasks".format(user_id))
            all_tasks_by_userId = get_user_tasks(conn, user_id, rDB)
            logging.debug("tasks retrieved successfully!")
            return all_tasks_by_userId

        elif method == "POST":
            logging.debug("trying to add one task to tasks")
            task_req_body = req.get_json()
            new_task_id = add_tasks(conn, task_req_body, user_id, rDB)
            logging.debug("task added successfully!")
            return new_task_id

        else:
            logging.warn(f"{method} method is not allowed for this endpoint")
            return func.HttpResponse(status_code=405)

    #displays erros encountered when API methods were called
    except Exception as e:
        return func.HttpResponse("Error: %s" % str(e), status_code=500)
    finally:
        conn.close()
        logging.debug('Connection to DB closed')


def connect_to_db():
    # Database credentials.
    redisFeature = os.environ["CACHE_TOGGLE"]
    server = os.environ["ENV_DATABASE_SERVER"]
    database = os.environ["ENV_DATABASE_NAME"]
    username = os.environ["ENV_DATABASE_USERNAME"]
    password = os.environ["ENV_DATABASE_PASSWORD"]
    driver = '{ODBC Driver 17 for SQL Server}'

    connection_string = "Driver={};Server={};Database={};Uid={};Pwd={};Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=30;".format(
        driver, server, database, username, password)
    return pyodbc.connect(connection_string)


def get_user_tasks(conn, userId, rDB):
    with conn.cursor() as cursor:
        logging.debug("execute query")
        cursor.execute("SELECT * FROM tasks WHERE userId=?", userId)

        logging.debug("Fetching all records")
        tasks = list(cursor.fetchall())

        # Clean up to put them in JSON.
        task_data = [tuple(task) for task in tasks]
        # Empty data list
        tasks = []
        columns = [column[0] for column in cursor.description]

    if(redisFeature):
        if(rDB.get('users:user_id:tasks:all')):
            unpacked_tasks = json.loads(rDB.get('tasks'))
            tasks = unpacked_tasks
            logging.debug('Tasks loaded from Redis')

        else:
            logging.debug('No tasks in Redis')

            for task in task_data:
                tasks.append(dict(zip(columns, task)))

            logging.debug("tasks received!!")

            #RedisLoad
            json_tasks = json.dumps(tasks);   
            rDB.set('users:user_id:tasks:all', json_tasks)

            return func.HttpResponse(json.dumps(tasks, default=default), status_code=200, mimetype="application/json")
    else:
        for task in task_data:
            tasks.append(dict(zip(columns, task)))
            
        logging.debug("tasks received!!")
        return func.HttpResponse(json.dumps(tasks, default=default), status_code=200, mimetype="application/json")


def add_tasks(conn, task_req_body, user_id, rDB):
    # First we want to ensure that the request has all the necessary fields
    logging.debug("Testing the add new user request body for necessary fields...")
    try:
        assert "title" in task_req_body, "New user request body did not contain field: 'title'"
        assert "description" in task_req_body, "New user request body did not contain field: 'description'"
    except AssertionError as task_req_body_content_error:
        logging.error("New user request body did not contain the necessary fields!")
        return func.HttpResponse(task_req_body_content_error.args[0], status_code=400)
    logging.debug("New task request body contains all the necessary fields!")

    if(redisFeature):
        rDB.expire('users:user_id:tasks:all')

    with conn.cursor() as cursor:
        # get task data
        userId = user_id
        title = task_req_body["title"]
        description = task_req_body["description"]
        createdDate = datetime.datetime.now()
        task_params = (userId, title, description, createdDate)
        # Create the query
        add_task_query = """
                         SET NOCOUNT ON;
                         DECLARE @NEWID TABLE(ID INT);
                         INSERT INTO tasks (userId, title, description, createdDate)
                         OUTPUT inserted.taskId INTO @NEWID(ID)
                         VALUES(?, ?, ?, ?);
                         SELECT ID FROM @NEWID
                         """
        logging.debug("execute query")
        cursor.execute(add_task_query, task_params)
        # Get the user id from cursor
        task_id = cursor.fetchval()
        logging.info(task_id)
        logging.debug("task with id {} added!".format(task_id))
        
        return func.HttpResponse(json.dumps({task_id}, default=default), status_code=200, mimetype="application/json")