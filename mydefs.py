import os
import logging
import boto3
import botocore
import platform
import time
from botocore.exceptions import ClientError

s3 = boto3.resource('s3')
global bucket_list
global counter
global region
bucket_list = []
file_list = []
locations_literal = ["us-east-1", "us-east-2", "us-west-1", "us-west-2"]
locations_nice = ["US East 1 - N. Virginia", "US East 2 - Ohio", "US West 1 - N. California", "US West 2 - Oregon"]
location = locations_literal[1]

def load_locations():
    counter = 0
    for x in locations_literal:
        print(str(counter) + ".", locations_nice[counter])
        counter += 1
    return ""

def load_buckets():
    bucket_list = []
    for buckets in s3.buckets.all():
        bucket_list.append(buckets.name)
    return bucket_list

def create_bucket(bucket_name, region):
    try:
        if region is None:
            s3.create_bucket(Bucket=bucket_name)
            print("Bucket created successfully.")
        else:
            location = {'LocationConstraint': region}
            s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
            print("Bucket created successfully.")
    except ClientError as err:
        logging.error(err)
        return False
    return True

def delete_object(bucket, objectkey):
    s3.Object(bucket, objectkey).delete()
    print("Removing: ", objectkey)

def delete_bucket(bucket):
    global mathcounter
    mathcounter = 0
    counter = 0
    for items in bucket.objects.all():
        counter += 1
    mathcounter = counter
    if counter >= 1:
        print("Bucket is not empty, removing all objects.")
        for items in bucket.objects.all():
            counter += 1
            print("Deleting: ", items.key)
            print(int((counter / mathcounter)*100), "% Done...")
            bucket.object(items.key).delete()
            time.sleep(1)
        print("All objects have been removed, now removing the bucket.")
    bucket.delete()
    print("Bucket has been removed.")

def upload_file(file_name, bucket, object_name=None):
    if object_name == None:
        object_name = os.path.basename(file_name)
        s3 = boto3.client('s3')
    try:
        response = s3.upload_file(file_name, bucket, object_name)
        time.sleep(3)
    except ClientError as err:
        logging.error(err)
        return False
    return True

def download_file(bucket, objectkey):
    try:
        bucket.download_file(objectkey, objectkey)
    except ClientError as err:
        if err.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

def clear_console():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')


def select_location():
    print(load_locations())
    location = input("What location would you like to work with?(Select the number, leave blank for default): \n -> ")
    if location != "":
        location = locations_literal[int(location)]
    return location

def get_location(bucket):
    s3 = boto3.client('s3')
    result = s3.get_bucket_location(Bucket=bucket)
    nice_location = ""
    counter = 0
    for place in locations_literal:
        if place == result["LocationConstraint"]:
            nice_location = locations_nice[int(counter)]
        counter += 1
    return nice_location
