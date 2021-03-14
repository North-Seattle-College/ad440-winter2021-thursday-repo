
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.create_db_instance

# https://aws.amazon.com/blogs/infrastructure-and-automation/deploy-cloudformation-stacks-at-the-click-of-a-button/ 

# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.create_stack

# TODO: need to resolve invalid client token issue when creating a stack. It looks like I have missing write privaleges to cloudformation in IAM
# Next, work on error handling and logging.
# My script
import boto3
import logging
from botocore.exceptions import ClientError

def deployTemplate():
    """Deploy RDS Stack using Cloudformation Template

    :return: response data from the stack deployment
    """
    # Prompt for secrets
    aws_access_key = input('aws access key: ')
    aws_access_secret = input('aws access secret: ')

    session = boto3.Session(
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_access_secret
    )
    logging.info(session)

    try:
        rds_client = session.client('cloudformation', region_name='us-west-2')
        return rds_client.create_stack(
            StackName="testing_stack_jb",
            TemplateURL="https://s3.us-west-2.amazonaws.com/cloudformation-templates-us-west-2/RDS_PIOPS.template"
        )
    except ClientError as e:
        # logging.error(e)
        raise e
    # return response_data

def main():
    
    response_data = deployTemplate()
    print(response_data)

main()


# import json
# import boto3
# import os
# from datetime import datetime
# from urllib.parse import urlparse

# params_url = os.environ['paramsFile']
# template_url = os.environ['templateUrl']

# def parse_params():
#   s3 = boto3.resource('s3')
#   s3_parse = urlparse(params_url)
#   bucket = s3_parse.netloc
#   s3_key = s3_parse.path.lstrip('/')
#   s3_obj = s3.Object(bucket, s3_key)
#   template_raw_data = s3_obj.get()["Body"].read().decode('utf-8')
#   template_params = json.loads(template_raw_data)
#   return template_params
  
# def launch_stack():
#   cfn = boto3.client('cloudformation')
#   current_ts = datetime.now().isoformat().split('.')[0].replace(':','-')
#   stackname = 'Iot-qs-deploy-' + current_ts
#   capabilities = ['CAPABILITY_IAM', 'CAPABILITY_AUTO_EXPAND']
#   try:
#     template_params = parse_params()
#     stackdata = cfn.create_stack(
#       StackName=stackname,
#       DisableRollback=True,
#       TemplateURL=template_url,
#       Parameters=template_params,
#       Capabilities=capabilities)
#   except Exception as e:
#     print(str(e))
#   return stackdata  

# def handler(event, context):
#   print("Received event:")
#   stack_result=launch_stack()
#   print(stack_result)