import logging
import pyodbc
import os
import azure.functions as func
import json
import redis

#Global value to be used to invalidate GET,PUT, and DELETE for Redis Cache
ALL_USERS_KEY = b'users:all'

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
        _redis = init_redis()
        # Return results according to the method
        if method == 'GET':
            logging.info('Attempting to retrieve user...')
            user_http_response = get_user(conn, user_id, _redis)
            logging.info('User retrieved successfully!')
            return user_http_response
        elif req.method == 'PUT':
            user_req_body = get_user_req_body(req)

            logging.info('Attempting to update (PUT) user...')
            updateUser = update_user(user_req_body, conn, user_id, _redis)

            return updateUser
        elif req.method == 'PATCH':
            user_req_body = get_user_req_body(req)

            logging.info('Attempting to update (PATCH) user...')
            patchUser = patch_user(user_req_body, conn, user_id, _redis)

            return patchUser
        elif method == 'DELETE':
            logging.info('Attempting to delete user...')
            deleteUser = delete_user(conn, user_id, _redis)

            return deleteUser
        else:
            logging.warn('''
              Request with method {} has been recieved,
              but that is not allowed for this endpoint
            '''.format(method))

            return func.HttpResponse('invalid request method', status_code=405)

    # displays errors encountered when API methods were called
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
    REDIS_HOST = os.environ['ENV_REDIS_HOST']
    REDIS_PORT = os.environ['ENV_REDIS_PORT']
    REDIS_KEY = os.environ['ENV_REDIS_KEY']

    return redis.StrictRedis(
      host=REDIS_HOST, port=REDIS_PORT, db=0, password=REDIS_KEY, ssl=True
    )


def get_user(conn, user_id, _redis):
    is_cachable = False
    try: 
        cache = get_user_cache(_redis)
        user = json.loads(cache)
        user_user_id = user['userId']

        #Calls invalidate method to see if data is cachable
        is_cachable = canInvalidate(cache, user_user_id, user_id)

        #Clears cache if data was not cachable
        if not is_cachable:
            clear_cache(_redis)

    except TypeError as e:
        logging.info(e.args[0])

    try:
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
                cache_user(_redis, user)

                respond = json.dumps(user)
                statuse_code = 200

        elif cache is not None:
            respond = cache.decode('utf-8')
            statuse_code = 200

    except TypeError as e:
        respond = 'get user failed'
        logging.info(respond)
        logging.info(e.args[0])
        statuse_code = 400

    return func.HttpResponse(
        respond,
        status_code=statuse_code,
        mimetype='application/json'
    )


def get_user_cache(_redis):
    try:
        cache = _redis.get(ALL_USERS_KEY)
        return cache
    except TypeError as e:
        logging.critical('Failed to fetch user from cache: ' + e.args[1])
        return None


def clear_cache(_redis):
    _redis.delete(ALL_USERS_KEY)


def cache_user(_redis, user):
    try:
        _redis.set(ALL_USERS_KEY, json.dumps(user), ex=1200)
        logging.info('Caching complete')
    except TypeError as e:
        logging.info('Caching failed')
        logging.info(e.args[0])


def update_user(user_req_body, conn, user_id, _redis):
    # Validate request body
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
        return func.HttpResponse(
          user_req_body_content_error.args[0], status_code=400
        )

    logging.debug('User request body contains all the necessary fields!')

    try:
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

            clear_cache(_redis)

            respond = 'User updated'
            statuse_code = 200

    except TypeError as e:
        respond = 'patch failed'
        logging.info(respond)
        logging.info(e.args[0])
        statuse_code = 400

    return func.HttpResponse(
        respond,
        status_code=statuse_code
    )


def patch_user(user_req_body, conn, user_id, _redis):
    logging.debug('''
      Going to execute PATCH query on user {}
    '''.format(user_id))

    fieldsToUpdate = list(user_req_body.keys())
    updatableFields = ['firstName', 'lastName', 'email']

    try:
        with conn.cursor() as cursor:
            if len(fieldsToUpdate) == 0:
                logging.critical('''
                  request body did not contain fields to update the user
                ''')

                respond = 'no field to update'
                statuse_code = 400

            elif set(fieldsToUpdate).issubset(updatableFields):
                fieldsInQuery = ''
                params = []

                for field in fieldsToUpdate:
                    comma = ' ' if field == fieldsToUpdate[-1] else ', '
                    params.append(user_req_body[field])

                    fieldsInQuery += "{} = ?{}".format(str(field), comma)

                sql_query = """
                  UPDATE users SET {} WHERE userId = ?
                """.format(fieldsInQuery)

                params.append(int(user_id))

                cursor.execute(sql_query, tuple(params))

                clear_cache(_redis)

                respond = 'user updated successfully'
                statuse_code = 200

            else:
                respond = 'invalid request body'
                statuse_code = 400

    except TypeError as e:
        respond = 'patch failed'
        logging.info(respond)
        logging.info(e.args[0])
        statuse_code = 400

    return func.HttpResponse(
        respond,
        status_code=statuse_code
    )


def delete_user(conn, user_id, _redis):
    
    clear_cache(_redis)
    try:
        with conn.cursor() as cursor:
            logging.debug('''
              Attempting to retrieve user by ID and delete the user...
            ''')

            delete_user_query = 'DELETE FROM users WHERE userId= ?'

            logging.debug('Executing query: ' + delete_user_query)

            cursor.execute(delete_user_query, (user_id))

            logging.debug('User was deleted successfully!.')


            respond = 'User deleted'
            statuse_code = 200
    except TypeError as e:
        respond = 'delete failed'
        logging.info(respond)
        logging.info(e.args[0])
        statuse_code = 400

    return func.HttpResponse(respond, status_code=statuse_code)


def get_user_req_body(req):
    user_req_body = dict()

    try:
        user_req_body = req.get_json()
    except ValueError:
        logging.error('Empty req body or non-JSON file passed')
        pass

    return user_req_body

def canInvalidate(cache, user_user_id, user_id):
    return cache is not None and int(user_user_id) == int(user_id)