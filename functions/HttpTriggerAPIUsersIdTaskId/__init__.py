import logging
import os
import pyodbc
import azure.functions as func

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

    conn_string = os.getenv('SQL_CONNECTION_STRING')
    cnxn = pyodbc.connect(conn_string)
    cursor = cnxn.cursor()
    logging.info('opened connection')

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

    if userId and taskId: 
        logging.info(f"Got userId:{userId} and taskId: {taskId}")

        sql_query = ('''SELECT tasks.title, tasks.description, CONCAT (users.firstName, ' ', users.lastName) AS "user" 
        FROM [dbo].[tasks] JOIN [dbo].[userTasks] on tasks.taskId = userTasks.taskId JOIN [dbo].[users] 
        on userTasks.userId = users.userId''')
        logging.info('Going to execute a query')
        cursor.execute(sql_query)
        logging.info('Executed the query')
        data = cursor.fetchall()
        logging.info(f"Got result: {data}")
        return func.HttpResponse(f"This {method} method was called. You entered {userId} as uId and {taskId} as taskId. Result: {data}")
    else:
        logging.info('Got only one of userId and taskId')
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a method, userId and taskId for an appropriate response.",
            status_code=200
        ) 
    logging.info('Finishing the function without error')
    return func.HttpResponse("Nothing done")