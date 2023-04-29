import boto3
import time

# Create a session with AWS using the default profile
session = boto3.Session()

# Set the S3 bucket name and prefix (if any)
bucket_name = 'sl546proj2output'

# Create an S3 client
s3 = session.client('s3')

# Get the current list of object keys
response = s3.list_objects_v2(Bucket=bucket_name)
if 'Contents' in response:
    object_keys = [obj['Key'] for obj in response['Contents']]
else:
    object_keys = []

print('Polling started...')

# Poll the S3 bucket every 60 seconds and download new objects
while True:
    # Wait for 60 seconds before checking again
    time.sleep(60)

    # Get the new list of object keys
    response = s3.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        new_object_keys = [obj['Key'] for obj in response['Contents']]
    else:
        new_object_keys = []

    # Find the difference between the current and new lists
    diff = list(set(new_object_keys) - set(object_keys))

    # Download the new objects
    for key in diff:
        s3.download_file(bucket_name, key, key)
        print('Download file: ' + key)

    # Update the current list of object keys
    object_keys = new_object_keys
