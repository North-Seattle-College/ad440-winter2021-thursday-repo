import boto3
import sys
import logging
from botocore.exceptions import ClientError

# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html 
# S3 Upload python script for users/id/tasks/id

def main():
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :return: True if file was uploaded, else False
    """

    # Variables from shell script
    bucket = sys.argv[1]
    aws_access_key = sys.argv[2]
    aws_access_secret = sys.argv[3]
    file_name = sys.argv[4]

    session = boto3.Session(
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_access_secret,
    )

    s3_client = session.client('s3')

    try:
        response = s3_client.upload_file(
            Filename = file_name,
            Bucket = bucket,
            Key = file_name # Object name default to file name
        )
    except ClientError as e:
        logging.error(e)
        return False
    return True


main()

