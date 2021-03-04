import boto3
from botocore.config import Config
from botocore.exceptions import ClientError, NoCredentialsError
from colorama import init, Fore
import argparse

parser = argparse.ArgumentParser(description="Deletes S3 buckets.")
parser.add_argument('--AccessKeyId', dest='aws_access_key_id', required=True)
parser.add_argument('--SecretAccessKey', dest='aws_secret_access_key', required=True)
parser.add_argument('--RegionName', dest='region_name', default='us-west-2', help='Region Name (default: us-west-2)')

args = parser.parse_args()

def main(aws_access_key_id, aws_secret_access_key, region_name):
    """
    The main function for the S3 bucket deletion script. 
    The account tied to the acccess key id and secret key must have permissions to read, list, and delete S3 buckets and objects.

    :param aws_access_key_id: the access key for the account you would like to connect to AWS with
    :type aws_access_key_id: str
    :param aws_secret_access_key: the secret key for the account you would like to connect to AWS with
    :type aws_secret_access_key: str
    :param region_name: the region of the S3 buckets you would like to delete
    :type region_name: str
    """
    
    # Some initial setup
    COL_SIZE = 15
    init(autoreset=True)

    print(Fore.GREEN + "Starting S3 bucket deletion script...")
    try:
        client_config = Config(
            region_name = region_name
        )

        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            config=client_config
        )

        print("Retrieving S3 bucket list...")
        list_buckets_response = s3_client.list_buckets()
        print(Fore.GREEN + "Bucket list retrieved! Cycling through list...")

        buckets_to_delete = []
        for bucket in list_buckets_response['Buckets']:
            bucket_name = bucket['Name']
            
            # Retrieve Bucket Information
            print(f'\nRetrieving bucket: {bucket_name} information...')
            bucket_owner_email = get_owner_email(s3_client, bucket_name)
            bucket_object_list = get_bucket_object_list(s3_client, bucket_name)

            # Display that information
            print(Fore.GREEN + f'{"Bucket:":<{COL_SIZE}}{bucket_name}')
            print(Fore.GREEN + f'{"OwnerEmail:":<{COL_SIZE}}{bucket_owner_email}')
            bucket_object_list_prepared_for_deletion = []
            if len(bucket_object_list) != 0:
                print(Fore.GREEN + "Bucket Objects:")
                # Display object information for the current bucket
                for bucket_object in bucket_object_list:
                    # Prepare just in case we want to delete the bucket
                    bucket_object_list_prepared_for_deletion.append({
                        'Key': bucket_object
                    })
                    print(bucket_object)
            
            # Prompt user for response
            delete_bucket_response = ""
            while delete_bucket_response == "":
                deletion_prompt_response = input(Fore.YELLOW + f'Delete bucket ({bucket_name}): (y/N/exit)')
                if deletion_prompt_response in ["y", "N", "exit"]:
                    delete_bucket_response = deletion_prompt_response
                else:
                    print(Fore.RED + 'Invalid command! Please use "y", "N", or "exit"!')

            if delete_bucket_response == "y":
                deletion_information = {
                    'BucketName': bucket_name,
                    'Objects': bucket_object_list_prepared_for_deletion
                }
                buckets_to_delete.append(deletion_information)
                print(Fore.GREEN + "Object scheduled for deletion!")
            elif delete_bucket_response == "exit":
                break
        
        # Delete the scheduled buckets
        if len(buckets_to_delete) > 0:
            print("\nAttempting to delete buckets scheduled for deletion...")
            delete_buckets(s3_client, buckets_to_delete)
            print(Fore.GREEN + "Buckets deleted! Exiting script.")
        else:
            print(Fore.GREEN + "No buckets scheduled for deletion. Exciting script")
        

    except (ClientError, NoCredentialsError)  as e:
        print(Fore.RED + f'Error connecting to S3! {e}')
    

def get_owner_email(s3_client, bucket_name):
    """
    Gets the owner's email of an S3 bucket if that information is included in the bucket tags as OwnerEmail
    
    :param s3_client: the client necessary to execute S3 commands
    :type s3_client: S3.Client
    :param bucket_name: the name of the bucket you would like the owner of
    :type bucket_name: str
    :returns: either the email of the owner of the bucket or No Owner if the no such email exists
    :rtype: str
    """
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
        return "No Owner"

def get_bucket_object_list(s3_client, bucket_name):
    """
    Gets the names of the objects in an S3 bucket returns them as a list

    :param s3_client: the client necessary to execute S3 commands
    :type s3_client: S3.Client
    :param bucket_name: the name of the bucket you would like the objects of
    :type bucket_name: str
    :returns: the list of object names
    :rtype: list
    """
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
        return {"error": e}
    

def delete_buckets(s3_client, buckets_to_delete_list):
    """
    Loops through a list of buckets, deletes the objects in each one (if any exist), and then deletes the bucket itself.

    :param s3_client: the client necessary to execute S3 commands
    :type s3_client: S3.Client    
    :param buckets_to_delete_list: a list of bucket names and bucket objects of the form 
        [{ 'BucketName': 'string', 'Objects': [{'Key': 'string'}] }]
    :type buckets_to_delete_list: list
    :returns: a dictionary containing either {"error": e} (if there was one) or {"success": True} if the deletion was successful
    :trype: dict
    """
    try:
        for bucket_to_delete in buckets_to_delete_list:
            print(f'Attempting to delete bucket: {bucket_to_delete["BucketName"]}...')

            if len(bucket_to_delete['Objects']) > 0:
                print("Bucket has objects, attempting to delete them...")
                objects_deletion_response = s3_client.delete_objects(
                    Bucket=bucket_to_delete['BucketName'],
                    Delete={
                        'Objects': bucket_to_delete['Objects']
                    }
                )
                print(Fore.GREEN + "Objects deleted!")
            
            bucket_deletion_response = s3_client.delete_bucket(
                Bucket=bucket_to_delete['BucketName']
            )

            print(Fore.GREEN + f'Bucket ({bucket_to_delete["BucketName"]}) deleted! \n')
    
        # Function completed successfully
        return {"success": True}

    except Exception as e:
        print(Fore.RED + f'Error while deleting buckets:  {e}')
        return {"error": e}

if __name__ == "__main__":
    main(args.aws_access_key_id, args.aws_secret_access_key, args.region_name)