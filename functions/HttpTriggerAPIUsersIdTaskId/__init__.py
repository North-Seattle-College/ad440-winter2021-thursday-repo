import logging
import os
import pyodbc
import azure.functions as func

def get(param1, param2):
    return func.HttpResponse(f'You passed in {param1}, {param2} values')
def post(param):
    return func.HttpResponse(f'You selected {param} method')
def update(param1, param2):
    return func.HttpResponse(f'You passed in {param1}, {param2} values')
def delete(param):
    return func.HttpResponse(f'You selected {param} method')


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
        
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

    method = req.method
    if not method:
        logging.critical('No method available')
        raise Exception('No method passed')
    if method == "GET":
        get(userId, taskId)
        conn_string = os.getenv('SQL_CONNECTION_STRING')
        cnxn = pyodbc.connect(conn_string)
        cursor = cnxn.cursor()
        logging.info('opened connection')        
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
        finally:
            cursor.close()
            cnxn.close()
            logging.info('Closed the connection')

    if method == "POST":
        post(method)
        # conn_string = os.getenv('SQL_CONNECTION_STRING')
        # cnxn = pyodbc.connect(conn_string)
        # cursor = cnxn.cursor()
        # logging.info('opened connection')        
        # logging.info('Going to execute a query')
        # try:
        #     #insert row into tasks table / create a new task
        #     #createdDate #'20120618 10:34:09 AM' and title/description are hardcoded for sprint1, update with automated date stamp and url params later
        #     sql_query = ("""INSERT INTO dbo.tasks (userId, title, description, createdDate)
        #     VALUES (?, ?, ?, '20120618 10:34:09 AM')""")
        #     cursor.execute(sql_query, userId, 'Do It', 'Almost like Nike motto')   
        #     logging.info('Executed the query')
        #     cnxn.commit()
        #     data = cursor.fetchall()
        #     logging.info(f"Got result: {data}")
        #     return func.HttpResponse(f"This {method} method was called. You entered {userId} as uId and {taskId} as taskId. Result: {data}")
        # except Exception as e:
        #     return func.HttpResponse("Error: %s" % str(e), status_code=500)
        # finally:
        #     cursor.close()
        #     cnxn.close()
        #     logging.info('Closed the connection')

    if method == "UPDATE":
        update(userId, taskId)
        conn_string = os.getenv('SQL_CONNECTION_STRING')
        cnxn = pyodbc.connect(conn_string)
        cursor = cnxn.cursor()
        logging.info('opened connection')        
        logging.info('Going to execute a query')
        try:
            #update task: title and description. Client passes userId and taskId, for sprint 1 other fields are hardcoded
            sql_query = ("""UPDATE [dbo].[tasks]
            SET title = 'Title updated by Natalia', description = 'Description updated by Natalia'
            WHERE userId = ? AND taskId = ?""")   
            rowcount = cursor.execute(sql_query, userId, taskId).rowcount
            logging.info(f"Executed the query: {rowcount} rows affected")
            cnxn.commit()
            return func.HttpResponse(f"This {method} method was called. You entered {userId} as uId and {taskId} as taskId. {rowcount} rows affected.")
        except Exception as e:
            return func.HttpResponse("Error: %s" % str(e), status_code=500)
        finally: 
            cursor.close()
            cnxn.close()
            logging.info('Closed the connection')

    if method == "DELETE":
        delete(method)
        # conn_string = os.getenv('SQL_CONNECTION_STRING')
        # cnxn = pyodbc.connect(conn_string)
        # cursor = cnxn.cursor()
        # logging.info('opened connection')        
        # logging.info('Going to execute a query')
        # try:
        #     # #delete row, client passes in userId and taskId
        #     sql_query = ("""DELETE FROM [dbo].[tasks] WHERE userId = ? AND taskId = ?""")
        #     cursor.execute(sql_query, userId, taskId)
        #     logging.info('Executed the query')
        #     cnxn.commit()
        #     data = cursor.fetchall()
        #     logging.info(f"Got result: {data}")
        #     return func.HttpResponse(f"This {method} method was called. You entered {userId} as uId and {taskId} as taskId. Result: {data}")
        # except Exception as e:
        #     return func.HttpResponse("Error: %s" % str(e), status_code=500)
        # finally:
        #     cursor.close()
        #     cnxn.close()

    else:
        logging.info('Got only one of userId and taskId')
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a method, userId and taskId for an appropriate response.",
            status_code=200
        ) 
    logging.info('Finishing the function without error')
    return func.HttpResponse("Nothing done")