import logging
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from colorama import init, Fore, Back

COL_SIZE = 15

logging.basicConfig(filename='example.log', level=logging.DEBUG)
init(autoreset=True)


def main():
    print(Fore.GREEN + "Starting S3 bucket deletion script...")
    try:
        s3_client = boto3.client('s3')
        
        print("Retrieving S3 bucket list...")
        list_buckets_response = s3_client.list_buckets()
        print(Fore.GREEN + "Bucket list retrieved! Cycling through list...\n")

        buckets_to_delete = []
        for bucket in list_buckets_response['Buckets']:
            bucket_name = bucket['Name']
            
            # Retrieve Bucket Information
            print(f'Retrieving bucket: {bucket_name} information...')
            bucket_owner_email = get_owner_email(s3_client, bucket_name)
            bucket_object_list = get_bucket_object_list(s3_client, bucket_name)

            # Display that information
            print(Fore.GREEN + f'{"Bucket:":<{COL_SIZE}}{bucket_name}')
            print(Fore.GREEN + f'{"OwnerEmail:":<{COL_SIZE}}{bucket_owner_email}')
            bucket_object_list_prepared_for_deletion = []
            if len(bucket_object_list) != 0:
                print(Fore.GREEN + "Bucket Objects:")
                for bucket_object in bucket_object_list:
                    bucket_object_list_prepared_for_deletion.append({
                        'KEY': bucket_object
                    })
                    print(bucket_object)
            
            # Prompt user for response
            received_delete_bucket_response = False
            while not received_delete_bucket_response:
                deletion_prompt_response = input(Fore.YELLOW + "Delete bucket: (y/N)")
                if (deletion_prompt_response == "y"):
                    deletion_information = {
                        'Bucket': bucket_name,
                        'Objects': bucket_object_list_prepared_for_deletion
                    }
                    buckets_to_delete.append(deletion_information)
                    print(Fore.GREEN + "Object scheduled for deletion!")
                    received_delete_bucket_response = True
                elif (deletion_prompt_response == "N"):
                    received_delete_bucket_response = True

            print()
        
        print(buckets_to_delete)

    except (ClientError, NoCredentialsError)  as e:
        print(Fore.RED + f'Error connecting to S3! {e}')
    

def get_owner_email(s3_client, bucket_name):
    try:
        get_bucket_tags_response = s3_client.get_bucket_tagging(
            Bucket=bucket_name
        )
                    
        bucket_owner_email_list = list(
            filter(
                lambda tag: tag['Key'] == "OwnerEmail",
                get_bucket_tags_response['TagSet']
            )
        )

        bucket_owner_email = "No Owner"
        if len(bucket_owner_email_list) == 1:
            bucket_owner_email = bucket_owner_email_list[0]['Value']

        return bucket_owner_email

    except s3_client.exceptions.from_code('NoSuchTagSetError') as e:
        print(Fore.YELLOW + "Bucket does not have any tags!")

def get_bucket_object_list(s3_client, bucket_name):
    try:
        get_bucket_object_list_response = s3_client.list_objects_v2(
            Bucket=bucket_name
        )

        bucket_object_list = []
        if ('Contents' in get_bucket_object_list_response):
            bucket_object_list = list(
                map(
                    lambda bucket_object: bucket_object['Key'],
                    get_bucket_object_list_response['Contents']
                )
            )
        else:
            print(Fore.YELLOW + "Bucket is empty!")

        return bucket_object_list

    except s3_client.exceptions.from_code('NoSuchBucket') as e:
        print(Fore.RED + "Bucket does not exist!")
    


def create_bucket(bucket_name):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the us-west-2.

    :param bucket_name: Bucket to create
    :return: True if bucket created, else False
    """
    
    region = 'us-west-2'

    # Create bucket
    try:
        s3_client = boto3.client('s3', region_name=region)
        location = {'LocationConstraint': region}
        acl = 'private'

        s3_client.create_bucket(
            Bucket=bucket_name,
            ACL=acl,
            CreateBucketConfiguration=location
        )
    
    except ClientError as e:
        logging.error(e)
        return False
    return True

main()