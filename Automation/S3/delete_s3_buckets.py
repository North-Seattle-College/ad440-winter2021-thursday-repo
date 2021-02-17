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
                    # Prepare just in case we want to delete the bucket
                    bucket_object_list_prepared_for_deletion.append({
                        'Key': bucket_object
                    })
                    print(bucket_object)
            
            # Prompt user for response
            delete_bucket_response = ""
            while delete_bucket_response == "":
                deletion_prompt_response = input(Fore.YELLOW + "Delete bucket: (y/N/exit)")
                if deletion_prompt_response == "y":
                    delete_bucket_response = "True"
                elif deletion_prompt_response == "N":
                    delete_bucket_response = "False"
                elif deletion_prompt_response == "exit":
                    delete_bucket_response = "Exit"

            
            if delete_bucket_response == "True":
                deletion_information = {
                    'BucketName': bucket_name,
                    'Objects': bucket_object_list_prepared_for_deletion
                }
                buckets_to_delete.append(deletion_information)
                print(Fore.GREEN + "Object scheduled for deletion!")
            elif delete_bucket_response == "Exit":
                break

            print()
        
        print()
        if len(buckets_to_delete) > 0:
            print("Attempting to delete buckets scheduled for deletion...")
            delete_buckets(s3_client, buckets_to_delete)
            print(Fore.GREEN + "Buckets deleted! Exiting script.")
        else:
            print(Fore.GREEN + "No buckets scheduled for deletion. Exciting script")
        

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
    

def delete_buckets(s3_client, buckets_to_delete_list):
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

            print(Fore.GREEN + "Bucket deleted! \n")

    except Exception as e:
        print(Fore.RED + f'Error while deleting buckets:  {e}')

main()