import json
import boto3
from datetime import datetime

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # Get bucket and object key from the event
    bucket_name = 'testbucketforwillhufall'
    table = dynamodb.Table('S3-object-size-history')

    # Get the list of all objects in the bucket
    response = s3.list_objects_v2(Bucket=bucket_name)
    
    total_size = 0
    object_count = 0

    if 'Contents' in response:
        for obj in response['Contents']:
            total_size += obj['Size']
            object_count += 1

    # Get current timestamp
    timestamp = datetime.utcnow().isoformat()

    # Store the bucket size info in DynamoDB
    table.put_item(
        Item={
            'timestamp': timestamp,
            'bucket_name': bucket_name,
            'total_size': total_size,
            'object_count': object_count
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Size-tracking lambda executed successfully')
    }
