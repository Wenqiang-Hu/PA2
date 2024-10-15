import boto3
import time
import requests

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = 'testbucketforwillhufall'

    # Create object
    s3.put_object(Bucket=bucket_name, Key='assignment1.txt', Body='Empty Assignment 1')
    time.sleep(2)

    # Update object
    s3.put_object(Bucket=bucket_name, Key='assignment1.txt', Body='Empty Assignment 2222222222')
    time.sleep(2)

    # Delete object
    s3.delete_object(Bucket=bucket_name, Key='assignment1.txt')
    time.sleep(2)

    # Create another object
    s3.put_object(Bucket=bucket_name, Key='assignment2.txt', Body='33')

    # Call plotting lambda via API Gateway
    api_url = 'https://tvunwnbhp6.execute-api.us-east-1.amazonaws.com/plot-func-stage/plot'  
    response = requests.get(api_url)

    return {
        'statusCode': 200,
        'body': response.text
    }
