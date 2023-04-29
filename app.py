import boto3
import json
import time
# Set up the S3 client
s3_client = boto3.client('s3')

# Set up the Lambda client
lambda_client = boto3.client('lambda')

# Set up the S3 bucket name and Lambda function name
bucket_name = 'sl546proj2'
lambda_function_name = 'getStudentInfo'

# Set up the S3 event that triggers the Lambda function
event = {
    'Records': [
        {
            's3': {
                'bucket': {'name': bucket_name},
                'object': {'key': ''}
            }
        }
    ]
}

# Continuously poll the S3 bucket for new files
while True:
    # Get a list of objects in the S3 bucket
    objects = s3_client.list_objects_v2(Bucket=bucket_name)

    # Check if any new objects have been uploaded since the last poll
    if objects['KeyCount'] > 0:
        # Get the name of the latest object
        latest_object = objects['Contents'][-1]['Key']

        # Update the Lambda function event with the name of the latest object
        event['Records'][0]['s3']['object']['key'] = latest_object

        print('Triggering lamda function!')
        # Invoke the Lambda function with the updated event
        response = lambda_client.invoke(
            FunctionName=lambda_function_name,
            InvocationType='Event',
            Payload=json.dumps(event)
        )

    # Wait for 1 minute before polling again
    time.sleep(30)