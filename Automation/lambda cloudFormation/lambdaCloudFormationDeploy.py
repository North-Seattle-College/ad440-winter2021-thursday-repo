import boto3
import sys
from botocore.exceptions import ClientError

def deployTemplate():
    """Deploy Lambda Function Stack using Cloudformation Template
    :param aws_access_key: The AWS key
    :param aws_access_secret: The AWS secret
    :returns: Response data from the stack deployment, 200 code if created
    """

    try:
        aws_access_key=sys.argv[1]
        aws_access_secret=sys.argv[2]
        stack_name=sys.argv[3]
        
    except Exception:
        print('\nIncorrect # of system arguments. Please re-check your parameters')
        return

    try:
        # Set up boto3 session
        session = boto3.Session(
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_access_secret
        )
        # CloudFormation call
        lambda_client = session.client('cloudformation', region_name='us-west-2')
        return lambda_client.create_stack(
            StackName=stack_name,
            TemplateURL="https://afrasiyab-sprint5.s3-us-west-2.amazonaws.com/template.json",
            Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM','CAPABILITY_AUTO_EXPAND']
        )
    except ClientError as e:
        raise(e)

def main():

    response_data = deployTemplate()

    if response_data != None and response_data['ResponseMetadata']['HTTPStatusCode'] == 200:
        print('Response Data: ', response_data)
        print('\nOperation Successful')
    else:
        print('\nAn error occurred, see above error message.')

main()