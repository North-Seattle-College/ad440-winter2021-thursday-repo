
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.create_db_instance

# https://aws.amazon.com/blogs/infrastructure-and-automation/deploy-cloudformation-stacks-at-the-click-of-a-button/ 

# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.create_stack

# TODO: need to resolve invalid client token issue when creating a stack. It looks like I have missing write privaleges to cloudformation in IAM
# Next, work on error handling and logging.

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

    # Set up boto3 session
    session = boto3.Session(
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_access_secret
    )

    ## Custom credential/config profile for easier testing
    # session = boto3.Session(
    #     profile_name="JB"
    # )
    # logging.info(session)

    try:
        rds_client = session.client('cloudformation', region_name='us-west-2')
        return rds_client.create_stack(
            StackName="testing_stack_jb",
            TemplateURL="https://s3.us-west-2.amazonaws.com/cloudformation-templates-us-west-2/RDS_PIOPS.template"
        )
    except ClientError as e:
        # logging.error(e)
        raise e

def main():
    
    response_data = deployTemplate()
    print(response_data)

main()
