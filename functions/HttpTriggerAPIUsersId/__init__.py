import logging
import pyodbc
import os
import azure.functions as func
import json
import redis


# This is the Http Trigger for Users/userId
# It connects to the db and retrives the users added to the db by userId
def main(req: func.HttpRequest) -> func.HttpResponse:
    method = req.method
    user_id = req.route_params.get('userId')

    logging.info(
      '''
        Python HTTP trigger for users/userId is
        processing a request to get user with id {}
      '''.format(user_id)
    )

    # Create a new connection
    logging.debug('Attempting DB connection!')
    try:
        conn = get_db_connection()
    except (pyodbc.DatabaseError, pyodbc.InterfaceError) as e:
        logging.critical('Failed to connect to DB: ' + e.args[0])
        logging.info('Error: ' + e.args[1])
        return func.HttpResponse(status_code=500)

    logging.debug('Connection to DB successful!')

    try:
        # Return results according to the method
        if method == 'GET':
            logging.info('Attempting to retrieve user...')
            user_http_response = get_user(conn, user_id, init_redis())
            logging.info('User retrieved successfully!')
            return user_http_response
        elif req.method == 'PUT':
            user_req_body = get_user_req_body(req)

            logging.info('Attempting to update (PUT) user...')

            return update_user(user_req_body, conn, user_id)
        elif req.method == 'PATCH':
            user_req_body = get_user_req_body(req)

            logging.info('Attempting to update (PATCH) user...')

            return patch_user(user_req_body, conn, user_id)
        elif method == 'DELETE':
            logging.info('Attempting to delete user...')

            return delete_user(conn, user_id)
        else:
            logging.warn('''
              Request with method {} has been recieved,
              but that is not allowed for this endpoint
            '''.format(method))

            return func.HttpResponse('invalid request method', status_code=405)

    # displays erros encountered when API methods were called
    except Exception as e:
        return func.HttpResponse('Error: %s' % str(e), status_code=500)
    finally:
        conn.close()
        logging.debug('Connection to DB closed')


def get_db_connection():
    # Connection String
    connection_string = os.environ['ENV_DATABASE_CONNECTION_STRING']

    return pyodbc.connect(connection_string)


def init_redis():
    REDIS_HOST = 'nsc-redis-dev-usw2-thursday.redis.cache.windows.net'
    REDIS_KEY = os.environ['ENV_REDIS_KEY']

    return redis.StrictRedis(
      host=REDIS_HOST, port=6380, db=0, password=REDIS_KEY, ssl=True
    )


def get_user(conn, user_id, init_redis):
    try:
        cache = get_user_cache(init_redis)
        user = json.loads(cache)
        user_user_id = user['userId']
        is_cachable = cache is not None and int(user_user_id) == int(user_id)
    except TypeError as e:
        logging.info(e.args[0])

    if (cache is None) or not is_cachable:
        with conn.cursor() as cursor:
            logging.debug(
                '''
                  Using connection cursor to execute query
                  (select user from users)
                '''
            )

            cursor.execute('SELECT * FROM users WHERE userId = ?', user_id)

            # Get user
            logging.debug('Fetching all queried information')
            user_data = list(cursor.fetchone())

            columns = [column[0] for column in cursor.description]
            user = dict(zip(columns, user_data))

            logging.debug(
                '''
                  User data retrieved and processed,
                  returning information from get_users function
                '''
              )

            logging.info('Caching results...')

            # Cache the results
            cache_user(init_redis, user)

            return func.HttpResponse(
              json.dumps(user), status_code=200, mimetype='application/json'
            )

    if cache is not None:
        return func.HttpResponse(
          cache.decode('utf-8'), status_code=200, mimetype='application/json'
        )


def get_user_cache(init_redis):
    try:
        cache = init_redis.get('user')
        return cache
    except TypeError as e:
        logging.critical('Failed to fetch user from cache: ' + e.args[1])
        return None


def cache_user(init_redis, user):
    try:
        init_redis.set('user', json.dumps(user), ex=1200)
        logging.info('Caching complete')
    except TypeError as e:
        logging.info('Caching failed')
        logging.info(e.args[0])


def update_user(user_req_body, conn, user_id):
    # Validate request body
    logging.debug('Verifying fields in request body to update a user by ID')
    try:
        assert 'firstName' in user_req_body, 'User request body did not contain field: "firstName"'
        assert 'lastName' in user_req_body, 'User request body did not contain field: "lastName"'
        assert 'email' in user_req_body, 'User request body did not contain field: "email"'
    except AssertionError as user_req_body_content_error:
        logging.error(
            'User request body did not contain the necessary fields!'
        )
        return func.HttpResponse(
          user_req_body_content_error.args[0], status_code=400
        )

    logging.debug('User request body contains all the necessary fields!')

    with conn.cursor() as cursor:
        # Unpack user data
        firstName = user_req_body['firstName']
        lastName = user_req_body['lastName']
        email = user_req_body['email']

        # Update user in DB
        update_user_query = '''
          UPDATE dbo.users SET firstName = ?,
          lastName = ?, email = ? WHERE userId= ?
        '''

        logging.debug('Executing query: ' + update_user_query)

        cursor.execute(
          update_user_query, (firstName, lastName, email, user_id)
        )

        logging.debug('User was updated successfully!.')

        return func.HttpResponse('User updated', status_code=200)


def patch_user(user_req_body, conn, user_id):
    logging.debug('''
      Going to execute PATCH query on user {}
    '''.format(user_id))

    fieldsToUpdate = list(user_req_body.keys())
    updatableFields = ['firstName', 'lastNAme', 'emeil']

    with conn.cursor() as cursor:
        if len(fieldsToUpdate) == 0:
            logging.critical('''
              request body did not contain fields to update the user
            ''')

            return func.HttpResponse('no field to update', status_code=400)
        elif set(fieldsToUpdate).issubset(updatableFields):
            fieldsInQuery = ''
            params = []

            for field in fieldsToUpdate:
                comma = ' ' if field == fieldsToUpdate[-1] else ', '
                params.append(field)

                fieldsInQuery += "{} = ?{}".format(str(field), comma)

            sql_query = """
              UPDATE users SET {} WHERE userId = ?
            """.format(fieldsInQuery)

            params.append(int(user_id))

            cursor.execute(sql_query, tuple(params))

            return func.HttpResponse(
                'user updated successfully',
                status_code=200,
                mimetype='application/json'
            )
        else:
            return func.HttpResponse('invalid request body', status_code=400)


def delete_user(conn, user_id):
    with conn.cursor() as cursor:
        logging.debug('''
          Attempting to retrieve user by ID and delete the user...
        ''')

        delete_user_query = 'DELETE FROM users WHERE userId= ?'

        logging.debug('Executing query: ' + delete_user_query)

        cursor.execute(delete_user_query, (user_id))

        logging.debug('User was deleted successfully!.')

        return func.HttpResponse('User deleted', status_code=200)


def get_user_req_body(req):
    user_req_body = dict()

    try:
        user_req_body = req.get_json()
    except ValueError:
        logging.error('Empty req body or non-JSON file passed')
        pass

    return user_req_body
