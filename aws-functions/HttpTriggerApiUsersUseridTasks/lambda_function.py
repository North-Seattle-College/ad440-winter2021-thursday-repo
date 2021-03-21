import os
import json
import logging
import pymysql
import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def default(dateHandle):
  if isinstance(dateHandle, (datetime.datetime, datetime.date)):
    return dateHandle.isoformat()
    
def lambda_handler(event, context):
    logger.info('Beginning function execution...')
    
    method = event['requestContext']['http']['method']
    userId = event['pathParameters']['userId']

    # Connect to the db
    db_name = os.environ['rds_db_name']
    
    logger.info(f'Attempting to connect to DB: {db_name}')
    
    try:
        conn = pymysql.connect(
          host = os.environ['rds_hostname'],
          user = os.environ['rds_username'],
          password = os.environ['rds_password'],
          database = os.environ['rds_db_name'],
          connect_timeout = 5
        )
    except pymysql.MySQLError as e:
        logger.error('ERROR: Unexpected error: Could not connect to MySQL instance.')
        logger.error(e)
        
        return {'statusCode': 500}
        
    logger.info('Connected to DB successfully!')
    
    # Respond to the method
    try:
        if method == 'GET':
            logger.info('Attempting to retrieve tasks...')

            all_tasks_http_response = get_tasks(conn, userId)
            
            logging.info(all_tasks_http_response)

            logger.info('tasks retrieved successfully!')
            
            return all_tasks_http_response
            
        elif method == 'POST':
            logging.info('Attempting to add task...')
            
            task_req_body = json.loads(event['body'])
            
            new_task_id_http_response = add_task(conn, task_req_body, userId)
            
            logging.info('task added successfully!')
            
            return new_task_id_http_response
            
        else:
            logging.warn(f'Request with method {method} has been recieved, but that is not allowed for this endpoint')
            
            return {'statusCode': 405}
            
    except Exception as e:
        return {
            'error': f'Error: {str(e)}',
            'statusCode': 500
        }
    
    finally: 
        conn.close()
        logging.debug('Connection to DB closed')
            
    logger.info('Function execution completed successfully!')

    
def get_tasks(conn, userId):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM tasks WHERE userId = %s", (userId))

        tasks_table = list(cursor.fetchall())
        tasks = []
        tasks_columns = [column[0] for column in cursor.description]

        for task in tasks_table:
            tasks.append(dict(zip(tasks_columns, task)))

    return json.dumps(tasks, default=default)


def add_task(conn, task_req_body, userId):
    logging.info('Testing the add new task request body for necessary fields...')

    try:
        assert "title" in task_req_body, "New task request body did not contain field: 'title'"
        assert "description" in task_req_body, "New task request body did not contain field: 'description'"
    
    except AssertionError as task_req_body_content_error:
        logging.critical('New task request body did not contain the necessary fields!')
        return {
          'error': task_req_body_content_error.args[0],
          'statusCode': 400
        }
    
    logging.info('New task request body contains all the necessary fields!')

    with conn.cursor() as cursor:
        # Unpack task data
        title = task_req_body['title']
        description = task_req_body['description']

        task_params = [userId, title, description]
        # Create the query
        add_task_query = """
                         INSERT INTO tasks (userId, title, description)
                         VALUES(%s, %s, %s);
                         """

        logging.info('Using connection cursor to execute query (add a new task and get id)')
        
        cursor.execute(add_task_query, task_params)
        conn.commit()
        
        # Get the task id from cursor
        task_id = cursor.lastrowid

        logging.info(
            f'task added and new task id ({task_id}) retrieved, returning information from add_task function'
        )
        
    return {'taskId': task_id}
