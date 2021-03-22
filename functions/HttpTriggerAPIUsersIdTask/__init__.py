import json
import pyodbc
import logging
import os
import azure.functions as func
import datetime
import redis 

redisFeature = "On" == os.environ["CACHE_TOGGLE"]

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(
        'Python HTTP trigger for /users/userId/tasks endpoint.')

    method = req.method
    user_id = req.route_params.get('userId')
    count = req.params.get('count')
    if (not count):
        count = "10"
    page = req.params.get('page')
    if (not page):
        page = "1"
    redis_key = "users:" + user_id + ":tasks&count=" + count + "&page=" + page

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
            rDBpassword = os.environ["ENV_REDIS_KEY"]
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
            all_tasks_by_userId = get_user_tasks(conn, user_id, count, page, r, redis_key)
            logging.debug("tasks retrieved successfully!")
            return all_tasks_by_userId

        elif method == "POST":
            logging.debug("trying to add one task to tasks")
            task_req_body = req.get_json()
            new_task_id = add_tasks(conn, task_req_body, user_id, r, redis_key)
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
    connection_string = os.environ["ENV_DATABASE_CONNECTION_STRING"]
    return pyodbc.connect(connection_string)

def get_user_tasks(conn, userId, count, page, r, redis_key):
    if (redisFeature): # Check cache first
        try:
            cache = get_user_tasks_cache(redis_key, r)
        except Exception as e:
            logging.info(e.args[0]) 

        if cache:
            logging.info("Returned data from cache")
            return func.HttpResponse(cache.decode('utf-8'), status_code=200, mimetype="application/json")
        else:         
            logging.info("Cache is empty, querying database...")

    with conn.cursor() as cursor:
        logging.info("Querying database...")
        lower_limit = (int(page) - 1) * int(count) 
        sql_query = "SELECT * FROM tasks WHERE userId=" + str(userId) + " ORDER BY taskId OFFSET " + str(lower_limit) + " ROWS FETCH NEXT " + str(count) + " ROWS ONLY"
        
        try:
            cursor.execute(sql_query)
        except Exception as e:
            logging.info("Error: " + e.args[1])

        tasks = list(cursor.fetchall())

        # Clean up to put them in JSON.
        task_data = [tuple(task) for task in tasks]

        # Empty data list
        tasks = []


        columns = [column[0] for column in cursor.description]

        for task in task_data:
            tasks.append(dict(zip(columns, task)))
            
        logging.debug(
            "User data retrieved and processed, returning information from get_user_tasks function")

        if (redisFeature):
            cache_user_tasks(r, redis_key, tasks)

        return func.HttpResponse(json.dumps(tasks, default=default), status_code=200, mimetype="application/json")

def cache_user_tasks(r, redis_key, tasks):
    if (redisFeature):
        try: 
            logging.info("Caching results...")
            r.set(redis_key, json.dumps(tasks), ex=1200)   
            logging.info("Caching complete")
        except TypeError as e:    
           logging.debug("Caching failed, serializing data and trying again...")
           r.set(redis_key, json.dumps(tasks, indent=4, sort_keys=True, default=str), ex=1200)
        except Exception as e:
            logging.info("Caching failed")
            logging.info(e.args[0])
              

def get_user_tasks_cache(redis_key, r):  
    if (redisFeature):
        logging.info("Querying cache...")
        try:
            cache = r.get(redis_key)
            return cache
        except Exception as e:
            logging.critical("Failed to fetch from cache: " + e.args[1])
            return None

def add_tasks(conn, task_req_body, user_id, r, redis_key):
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
        r.expire(redis_key)

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

# to handle datetime with JSON
# It serialize datetime by converting it into string
def default(dateHandle):
  if isinstance(dateHandle, (datetime.datetime, datetime.date)):
    return dateHandle.isoformat()

def init_redis():
    try:
        rDBpassword = os.environ["ENV_REDIS_KEY"]
        rDBhost = os.environ["ENV_REDIS_HOST"]
        rDBport = os.environ["ENV_REDIS_PORT"]
        rDB = redis.Redis(host=rDBhost, port=rDBport, db=0, password=rDBpassword, ssl=True) 
        logging.info("Connected to Redis")
        return rDB
    except(redis.exceptions.ConnectionError, ConnectionRefusedError) as e:
        logging.error("Redis connection error" + e.args[0])
