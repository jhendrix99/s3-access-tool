import mydefs
import time

def main_menu():
    bucket_list = []
    mydefs.clear_console()
    print("Basic S3 Control Tool - Welcome, " + mydefs.os.getlogin() + ".")
    print(" 1. Create Bucket \n 2. Delete Bucket(Dangerous) \n 3. Upload File \n 4. Download File \n 5. Delete File")
    menu_selection = input("What would you like to do?(1-5): \n -> ")
    menu_selection = int(menu_selection)
    if menu_selection == 1:
        location = mydefs.select_location()
        print(str(location))
        bucket_name = input("What would you like the new bucket to be called? \n -> ")
        mydefs.create_bucket(bucket_name, location)
    elif menu_selection == 2:
        bucket_list = []
        bucket_list = mydefs.load_buckets()
        if len(bucket_list) == 0:
            print("No buckets found.")
            mydefs.clear_console()
            main_menu()
        curcount = 0
        for bucket in bucket_list:
            print(mydefs.get_location(bucket), "\n", curcount, " ", bucket)
            curcount += 1
        bucketName = input("Which bucket would you like to remove?(Select Number): ")
        bucket = bucket_list[int(bucketName)]
        bucket = mydefs.s3.Bucket(bucket)
        print("Running this command will permanently remove all files in the bucket and the bucket itself.")
        verify = input("Are you sure you want to remove this bucket and all of its contents? Type '"'permanently delete'"' \n")
        if verify.upper() == "PERMANENTLY DELETE":
            mydefs.delete_bucket(bucket)
        else:
            print("Aborting...")
        time.sleep(3)
        mydefs.clear_console()
        main_menu()
    elif menu_selection == 3:
        bucket_list = mydefs.load_buckets()
        if len(bucket_list) == 0:
            print("No buckets found. Please make a new bucket first.")
            time.sleep(3)
            mydefs.clear_console()
            main_menu()

        #checking number of buckets to figure out what to do        
        if len(bucket_list) == 0:
            bucket = input("No buckets currently exist, please create one: \n -> ")
            print("You chose: ", bucket)
            mydefs.create_bucket(bucket)
        else:
            curcount = 0
            for bucket in bucket_list:
                print(mydefs.get_location(bucket), "\n", curcount, " ", bucket)
                curcount += 1
            bucket = input("Which bucket would you like to access?(Select Number): ")
            bucket = bucket_list[int(bucket)]

        file_name = input("Enter the location of the file to upload: ")
        print("You selected: ", mydefs.os.path.basename(file_name))

        print("Uploading your file, please wait...")
        mydefs.upload_file(file_name, bucket)
        print("Upload Complete!")
        time.sleep(3)
        mydefs.clear_console()
        main_menu()
    elif menu_selection == 4:
        bucket_list = mydefs.load_buckets()
        if len(bucket_list) == 0:
            print("No data found, going back to main menu.")
            time.sleep(3)
            mydefs.clear_console()
            main_menu()
        curcount = 0
        for bucket in bucket_list:
            print(curcount, " ", bucket)
            curcount += 1
        bucketName = input("Which bucket would you like to access?(Select Number): ")
        bucketName = bucket_list[int(bucketName)]
        bucket = mydefs.s3.Bucket(bucketName)
        curcount = 0
        for s3_files in bucket.objects.all():
            print(curcount, s3_files.key)
            mydefs.file_list.append(s3_files.key)
            curcount += 1
        if curcount == 0:
            print("No files found in bucket:", bucket.name)
            time.sleep(3)
            mydefs.clear_console()
            main_menu
        objectkey = input("Which file would you like to download?(Select number): ")
        mydefs.download_file(bucket, mydefs.file_list[int(objectkey)])
        print("File: ", mydefs.file_list[int(objectkey)], " has been downloaded!")
        time.sleep(3)
        mydefs.clear_console()
        main_menu()
    elif menu_selection == 5:
        bucket_list = mydefs.load_buckets()
        if len(bucket_list) == 0:
            print("No buckets found.")
            time.sleep(3)
            mydefs.clear_console()
            main_menu()
        curcount = 0
        for bucket in bucket_list:
            print(curcount, " ", bucket)
            curcount += 1

        bucketName = input("Which bucket would you like to access?(Select Number): ")
        bucketName = bucket_list[int(bucketName)]
        bucket = mydefs.s3.Bucket(bucketName)
        curcount = 0
        for s3_files in bucket.objects.all():
            print(curcount, s3_files.key)
            mydefs.file_list.append(s3_files.key)
            curcount += 1
        objectkey = input("Which file would you like to delete?(Select a number): ")
        mydefs.delete_object(bucketName, mydefs.file_list[int(objectkey)])
        print("The file was deleted!")
        time.sleep(1)
        mydefs.clear_console()
        main_menu()

main_menu()