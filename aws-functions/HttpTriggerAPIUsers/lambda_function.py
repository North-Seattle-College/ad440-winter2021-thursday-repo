import os
import json
import logging
import pymysql

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info('Beginning function execution...')
    method = event['requestContext']['http']['method']
    
    # Check that there actually is a method
    if not method:
        print("No method available")
        raise Exception('No method passed')
        
    logger.info(f'Function triggered with {method} method...')

    # Connect to the db
    db_name = os.environ['rds_db_name']
    logger.info(f'Attempting to connect to DB: {db_name}')
    try:
        conn = get_db_connection()
    except pymysql.MySQLError as e:
        logger.error('ERROR: Unexpected error: Could not connect to MySQL instance.')
        logger.error(e)
        return {
            'statusCode': 500
        }
    logger.info('Connected to DB successfully!')
    
    # Respond to the method
    try:
        if method == 'GET':
            logger.info('Attempting to retrieve users...')
            all_users_http_response = get_users(conn)
            logger.info('Users retrieved successfully!')
            return all_users_http_response
            
        elif method == 'POST':
            logging.info('Attempting to add user...')
            user_req_body = json.loads(event['body'])
            new_user_id_http_response = add_user(conn, user_req_body)
            logging.info('User added successfully!')
            return new_user_id_http_response
            
        else:
            logging.warn(f'Request with method {method} has been recieved, but that is not allowed for this endpoint')
            return {
                'statusCode': 405
            }
            
    #displays erros encountered when API methods were called
    except Exception as e:
        return {
            'error': f'Error: {str(e)}',
            'statusCode': 500
        }
    
    finally: 
        conn.close()
        logging.debug('Connection to DB closed')
            
    logger.info('Function execution completed successfully!')

def get_db_connection():
    conn = pymysql.connect(
        host            = os.environ['rds_hostname'],
        user            = os.environ['rds_username'],
        password        = os.environ['rds_password'],
        database        = os.environ['rds_db_name'],
        connect_timeout = 5
    )
    
    return conn
    
def get_users(conn):
    with conn.cursor() as cursor:
        logger.info(
            'Using connection cursor to execute query (select all from users)'
        )
        cursor.execute("SELECT * FROM users")
        
        # Get users
        logging.debug("Fetching all queried information")
        users_table = list(cursor.fetchall())

        # Clean up to put them in JSON.
        users_data = [tuple(user) for user in users_table]

        # Empty data list
        users = []

        users_columns = [column[0] for column in cursor.description]
        for user in users_data:
            users.append(dict(zip(users_columns, user)))
        
        logging.debug(
            "User data retrieved and processed, returning information from get_users function"
        )
        
        return json.dumps(users)

def add_user(conn, user_req_body):
    # First we want to ensure that the request has all the necessary fields
    logging.info('Testing the add new user request body for necessary fields...')
    try:
        assert 'firstName' in user_req_body, \
            "New user request body did not contain field: 'firstName'"
        assert 'lastName' in user_req_body, \
            "New user request body did not contain field: 'lastName'"
        assert 'email' in user_req_body, \
            "New user request body did not contain field: 'email'"
    
    except AssertionError as user_req_body_content_error:
        logging.critical('New user request body did not contain the necessary fields!')
        return {
          'error': user_req_body_content_error.args[0],
          'statusCode': 400
        }
    
    logging.info('New user request body contains all the necessary fields!')
    with conn.cursor() as cursor:
        # Unpack user data
        firstName = user_req_body['firstName']
        lastName = user_req_body['lastName']
        email = user_req_body['email']

        user_params = [firstName, lastName, email]
        # Create the query
        add_user_query = """
                         INSERT INTO users (firstName, lastName, email)
                         VALUES(%s, %s, %s);
                         """

        logging.info(
            'Using connection cursor to execute query (add a new user and get id)'
        )
        
        cursor.execute(add_user_query, user_params)
        conn.commit()
        
        # Get the user id from cursor
        user_id = cursor.lastrowid

        logging.info(
            f'User added and new user id ({user_id}) retrieved, returning information from add_user function'
        )
        
        return {
            'userId': user_id,
        }