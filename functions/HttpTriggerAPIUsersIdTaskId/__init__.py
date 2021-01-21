import logging
import os
import pyodbc
import azure.functions as func

#req.params.get
# def get(cursor, userId, taskId):
#     logging.info("GET method was called")
#     sql_query = f'SELECT description from [].[tasks] WHERE userID == {userId} AND taskId == {taskId}
#     cursor.execute(sql_query)
#     return 
# def post(cnxn, cursor, taskId, userId, assignedDate, completed, title, description, createdTime, deleted)):
#     logging.info("POST method was called")
#     sql_query1 = f'INSERT INTO [].[userTasks] VALUES ({taskId}, {userId}, {assignedDate}, {completed}')
#     sql_query2 = f'INSERT INTO [].[tasks] VALUES ({taskId}, {title}, {description}, {createdTime}, {deleted}')
#     cursor.execute(sql_query1)
#     cursor.execute(sql_query2)
#     cnxn.commit()
#     return 'POST executed'
# def update(method):
#     return func.HttpResponse(f"This update = {method} was called")
# def delete(method):
#     return func.HttpResponse(f"This delete = {method} was called")
def get(param):
    return (f'You selected {param} method')
def post(param):
    return (f'You selected {param} method')
def update(param):
    return (f'You selected {param} method')
def delete(param):
    return (f'You selected {param} method')


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # try:

    #db_username = os.environ["ENV_DATABASE_USERNAME"]
    #db_password = os.environ["ENV_DATABASE_PASSWORD"]
    #sql_query  = 'select top 1 * from [SalesLT].[Customer]' 
    ##test = os.getenv("TEST123")
    conn_string = os.getenv('SQL_CONNECTION_STRING')
    cnxn = pyodbc.connect(conn_string)
    cursor = cnxn.cursor()
    logging.info('opened connection')
    #cursor.execute(sql_query)
    #row = cursor.fetchone()
    #return func.HttpResponse(f"Rows: {row}")


    method = req.method
    if not method:
        logging.critical('No method available')
        raise Exception('No method passed')

    if method == "GET":
        get(method)
    if method == "POST":
        post(method)
    if method == "UPDATE":
        update(method)
    if method == "DELETE":
        delete(method)
        
    userId = req.params.get('userId')
    taskId = req.params.get('taskId')
    logging.info('Trying to get userId and taskId')
    if (not userId) and (not taskId):
        logging.info("Didn't get neither userId nor taskId")
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            userId = req_body.get('userId')
            taskId = req_body.get('taskId')
#'20120618 10:34:09 AM'
    if userId and taskId: 
        logging.info(f"Got userId:{userId} and taskId: {taskId}")

        # sql_query0 = ('''SELECT * FROM [dbo].[tasks]''')


        # sql_query1 = ('''SELECT tasks.title, tasks.description, CONCAT (users.firstName, ' ', users.lastName) AS "user" 
        # FROM [dbo].[tasks] JOIN [dbo].[users] 
        # on tasks.userId = users.userId WHERE users.userId = 1 AND tasks.taskId = 1''')

        #insert row
        #createdDate hardcoded for sprint1, update with automated date stamp later
        # sql_query2 = ('''INSERT INTO dbo.tasks (userId, title, description, createdDate)
        # VALUES (1, 'Do It', 'Almost like Nike motto', '20120618 10:34:09 AM')''')
            # # cursor.close ()
            # # conn.commit ()
            # # conn.close ()
        # #update task: title and description. Client passes userId and taskId
        # sql_query3 = ('''UPDATE [dbo].[tasks]
        # SET title = 'Title updated by Natalia', description = 'Description updated by Natalia'
        # WHERE userId =1 AND taskId =1''')        
        # #delete row
        # sql_query4 = ('''DELETE FROM [dbo].[tasks] WHERE userId =1 AND taskId =13''')
        
        logging.info('Going to execute a query')
        try:
            #Get task title, description and user name by userId and taskId
            sql_query = ("""SELECT tasks.title, tasks.description, CONCAT (users.firstName, ' ', users.lastName) AS "user" 
            FROM [dbo].[tasks] JOIN [dbo].[users] 
            on [dbo].[tasks].userId = [dbo].[users].userId
            WHERE [dbo].[users].userId = ? AND [dbo].[tasks].taskId = ?""")
            cursor.execute(sql_query, userId, taskId)
            logging.info('Executed the query')
            data = cursor.fetchall()
            logging.info(f"Got result: {data}")
            return func.HttpResponse(f"This {method} method was called. You entered {userId} as uId and {taskId} as taskId. Result: {data}")
        except Exception as e:
            return func.HttpResponse("Error: %s" % str(e), status_code=500)
    # cursor.close ()
    # conn.close ()

    else:
        logging.info('Got only one of userId and taskId')
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a method, userId and taskId for an appropriate response.",
            status_code=200
        ) 
    logging.info('Finishing the function without error')
    return func.HttpResponse("Nothing done")


    
    # except Exception as e:
    #     logging.critical(e)
    #     return func.HttpResponse(
    #             "Error: " + e,
    #             status_code=500
    #         ) 