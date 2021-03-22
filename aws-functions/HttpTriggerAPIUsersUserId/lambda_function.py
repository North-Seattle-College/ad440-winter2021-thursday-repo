import logging
import os
import json
import pymysql
​
​
logger = logging.getLogger()
logger.setLevel(logging.INFO)
​
​
def handler(event, context):
    logger.info('Beginning function execution...')
    logging.info(event)
​
    # method = event['httpMethod']
    method = event['requestContext']['http']['method']
    user_id = event['pathParameters']['userId']
​
    logging.info(
      '''
        Python HTTP trigger for users/userId is
        processing a request to {} user with id {}
      '''.format(method, user_id)
    )
​
    try:
        logging.info(os.environ['rds_hostname'])
        logging.info(os.environ['rds_username'])
        logging.info(os.environ['rds_password'])
        logging.info(os.environ['rds_db_name'])
​
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
        return {
            'statusCode': 500
        }
​
    logger.info('Connected to DB successfully!')
​
    # Respond to the method
    try:
        if method == 'GET':
            logging.info('Attempting to retrieve user...')
            user_http_response = get_user(conn, user_id)
            logging.info('User retrieved successfully!')
            return user_http_response
        elif method == 'PUT':
            user_req_body = json.loads(event['body'])
​
            logging.info('Attempting to update (PUT) user...')
​
            return update_user(user_req_body, conn, user_id)
        elif method == 'PATCH':
            user_req_body = json.loads(event['body'])
​
            logging.info('Attempting to update (PATCH) user...')
​
            return patch_user(user_req_body, conn, user_id)
        elif method == 'DELETE':
            logging.info('Attempting to delete user...')
​
            return delete_user(conn, user_id)
        else:
            logging.warn('''
              Request with method {} has been recieved,
              but that is not allowed for this endpoint
            '''.format(method))
​
            return {'statusCode': 405}
​
    except Exception as e:
        return {
            'error': f'Error: {str(e)}',
            'statusCode': 500
        }
​
    finally:
        conn.close()
        logging.debug('Connection to DB closed')
​
    logger.info('Function execution completed successfully!')
​
​
def get_user(conn, user_id):
    try:
        with conn.cursor() as cursor:
            logging.debug(
                '''
                  Using connection cursor to execute query
                  (select user from users)
                '''
            )
​
            cursor.execute('SELECT * FROM users WHERE userId = %s', user_id)
            conn.commit()
​
            # Get user
            logging.debug('Fetching all queried information')
            user_data = list(cursor.fetchone())
            columns = [column[0] for column in cursor.description]
            user = dict(zip(columns, user_data))
​
            logging.debug(
                '''
                  User data retrieved and processed,
                  returning information from get_users function
                '''
              )
​
            respond = json.dumps(user)
            statuse_code = 200
​
    except TypeError as e:
        respond = 'get user failed'
        logging.info(respond)
        logging.info(e.args[0])
        statuse_code = 400
​
    return {
        'statusCode': statuse_code,
        'body': respond,
        'headers': {"Content-Type": "application/json"}
    }
​
​
def update_user(user_req_body, conn, user_id):
    logging.debug('Verifying fields in request body to update a user by ID')
    try:
        assert 'firstName' in user_req_body, 'User request body did not contain field: "firstName"'
        assert 'lastName' in user_req_body, 'User request body did not contain field: "lastName"'
        assert 'email' in user_req_body, 'User request body did not contain field: "email"'
    except AssertionError as user_req_body_content_error:
        logging.error(user_req_body_content_error.args[0])
        logging.error(
            'User request body did not contain the necessary fields!'
        )
        return {
            'statusCode': 400,
            'body': user_req_body_content_error.args[0]
        }
​
    logging.debug('User request body contains all the necessary fields!')
​
    try:
        with conn.cursor() as cursor:
            # Unpack user data
            firstName = user_req_body['firstName']
            lastName = user_req_body['lastName']
            email = user_req_body['email']
​
            # Update user in DB
            update_user_query = '''
              UPDATE users SET firstName = %s,
              lastName = %s, email = %s WHERE userId= %s
            '''
​
            logging.debug('Executing query: ' + update_user_query)
​
            cursor.execute(
              update_user_query, [firstName, lastName, email, user_id]
            )
            conn.commit()
​
            logging.debug('User was updated successfully!.')
​
            respond = 'User updated'
            statuse_code = 200
​
    except TypeError as e:
        respond = 'put failed'
        logging.info(respond)
        logging.info(e.args[0])
        statuse_code = 400
​
    return {
        'statusCode': statuse_code,
        'body': respond,
        'headers': {"Content-Type": "application/json"}
    }
​
​
def patch_user(user_req_body, conn, user_id):
    logging.debug('''
      Going to execute PATCH query on user {}
    '''.format(user_id))
​
    fieldsToUpdate = list(user_req_body.keys())
    updatableFields = ['firstName', 'lastName', 'email']
​
    try:
        with conn.cursor() as cursor:
            if len(fieldsToUpdate) == 0:
                logging.critical('''
                  request body did not contain fields to update the user
                ''')
​
                respond = 'no field to update'
                statuse_code = 400
​
            elif set(fieldsToUpdate).issubset(updatableFields):
                fieldsInQuery = ''
                params = []
​
                for field in fieldsToUpdate:
                    comma = ' ' if field == fieldsToUpdate[-1] else ', '
                    params.append(user_req_body[field])
​
                    fieldsInQuery += "{} = %s{}".format(str(field), comma)
​
                sql_query = """
                  UPDATE users SET {} WHERE userId = %s
                """.format(fieldsInQuery)
​
                params.append(int(user_id))
​
                cursor.execute(sql_query, tuple(params))
                conn.commit()
​
                respond = 'user updated successfully'
                statuse_code = 200
​
            else:
                respond = 'invalid request body'
                statuse_code = 400
​
    except TypeError as e:
        respond = 'patch failed'
        logging.info(respond)
        logging.info(e.args[0])
        statuse_code = 400
​
    return {
        'statusCode': statuse_code,
        'body': respond,
        'headers': {"Content-Type": "application/json"}
    }
​
​
def delete_user(conn, user_id):
    try:
        with conn.cursor() as cursor:
            logging.debug('''
              Attempting to retrieve user by ID and delete the user...
            ''')
​
            delete_user_query = 'DELETE FROM users WHERE userId= %s'
​
            logging.debug('Executing query: ' + delete_user_query)
​
            cursor.execute(delete_user_query, (user_id))
​
            logging.debug('User was deleted successfully!.')
​
            respond = 'User deleted'
            statuse_code = 200
    except TypeError as e:
        respond = 'delete failed'
        logging.info(respond)
        logging.info(e.args[0])
        statuse_code = 400
​
    return {
        'statusCode': statuse_code,
        'body': respond,
        'headers': {"Content-Type": "application/json"}
    }