import os
import logging
import boto3
import botocore
import platform
import time
from botocore.exceptions import ClientError

s3 = boto3.resource('s3')
global buckets_list
buckets_list = []
file_list = []
global counter 
counter = 0
region = "us-east-2"

for buckets in s3.buckets.all():
    buckets_list.append(buckets.name)

def upload_file(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def create_bucket(bucket_name):
    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
            print("The bucket was created!")
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
            print("The bucket was created!")
    except ClientError as e:
        logging.error(e)
        return False
    return True
    menu_options()

def delete_object(bucket, objectKey):
    s3.Object(bucket, objectKey).delete()
    print("Removing: ", objectKey)

def delete_bucket(bucket):
    counter = 0
    for item in bucket.objects.all():
        counter += 1
    print(counter)
    if counter >= 1:
        print("Bucket is not empty, deleting all files.")
        for item in bucket.objects.all():
            bucket.Object(item.key).delete()
            print("Deleting: ", item.key)
        print("All items have been removed, now deleting bucket.")
    bucket.delete()
    print("Bucket deleted!")

def download_file(bucket, objectkey):
    try:
        bucket.download_file(objectkey, objectkey)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

def clear_console():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system()

def menu_options():
    buckets_list = []
    for buckets in s3.buckets.all():
        buckets_list.append(buckets.name)
    counter = 0
    print("Welcome to the basic S3 client!")
    print(" 1. Create New Bucket \n 2. Upload New File \n 3. Delete an Existing File \n 4. Download File \n 5. Delete Bucket(Dangerous)")
    menu_selection = input("What would you like to do?(1-5): ")
    menu_selection = int(menu_selection)
    #Create bucket option
    if menu_selection == 1:
        bucket_name = input("What would you like the new bucket to be called? \n")
        create_bucket(bucket_name)
        print("Bucket: ", bucket_name, " has been created!")
        time.sleep(3)
        clear_console()
        menu_options()

    #upload file option
    elif menu_selection == 2:
        print("THIS IS HAVING ISSUES ON WINDOWS")
        #checking number of buckets to figure out what to do        
        if len(buckets_list) == 0:
            bucketName = input("No buckets currently exist, please create one: ")
            print("You chose: ", bucketName)
            create_bucket(bucketName)
            bucket = bucketName
        else:
            curcount = 0
            for bucket in buckets_list:
                print(curcount, " ", bucket)
                curcount += 1
            bucketName = input("Which bucket would you like to access?(Select Number): ")
            bucketName = int(bucketName)

        file_name = input("Enter the location of the file to upload: ")
        print("You selected: ", os.path.basename(file_name))

        print("Uploading your file, please wait...")
        upload_file(file_name, bucket)
        print("Upload Complete!")
        time.sleep(3)
        clear_console()
        menu_options()
    #Delete an object option
    elif menu_selection == 3:
        curcount = 0
        for bucket in buckets_list:
            print(curcount, " ", bucket)
            curcount += 1
        bucketName = input("Which bucket would you like to access?(Select Number): ")
        bucketName = buckets_list[int(bucketName)]
        bucket = s3.Bucket(bucketName)
        curcount = 0
        for s3_files in bucket.objects.all():
            print(curcount, s3_files.key)
            file_list.append(s3_files.key)
            curcount += 1
        if curcount == 0:
            print("No files found in bucket:", bucket.name)
            time.sleep(3)
            clear_console()
            menu_options()
        objectkey = input("Which file would you like to delete?(Select a number): ")
        delete_object(bucketName, file_list[int(objectkey)])
        print("The file was deleted!")
        time.sleep(3)
        clear_console()
        menu_options()
    elif menu_selection == 4:
        curcount = 0
        for bucket in buckets_list:
            print(curcount, " ", bucket)
            curcount += 1
        bucketName = input("Which bucket would you like to access?(Select Number): ")
        bucketName = buckets_list[int(bucketName)]
        bucket = s3.Bucket(bucketName)
        curcount = 0
        for s3_files in bucket.objects.all():
            print(curcount, s3_files.key)
            file_list.append(s3_files.key)
            curcount += 1
        if curcount == 0:
            print("No files found in bucket:", bucket.name)
            time.sleep(3)
            clear_console()
            menu_options()
        objectkey = input("Which file would you like to download?(Select number): ")
        download_file(bucket, file_list[int(objectkey)])
        print("File: ", file_list[int(objectkey)], " has been downloaded!")
        time.sleep(3)
        clear_console()
        menu_options()
    elif menu_selection == 5:
        curcount = 0
        for bucket in buckets_list:
            print(curcount, " ", bucket)
            curcount += 1
        bucketName = input("Which bucket would you like to remove?(Select Number): ")
        bucketName = buckets_list[int(bucketName)]
        bucket = s3.Bucket(bucketName)
        print("Running this command will permanently remove all files in the bucket and the bucket itself.")
        verify = input("Are you sure you want to remove this bucket and all of its contents? Type '"'permanently delete'"' \n")
        if verify.upper() == "PERMANENTLY DELETE":
            delete_bucket(bucket)
        else:
            print("Aborting...")
        time.sleep(3)
        clear_console()
        menu_options()
    else:
        exit()
menu_options()