import json
import boto3
import matplotlib.pyplot as plt
from io import BytesIO
import time
from datetime import datetime, timedelta
`
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

def query_dynamodb(bucket_name, table_name):
    table = dynamodb.Table(table_name)
    current_time = datetime.now()
    ten_seconds_ago = current_time - timedelta(seconds=10)
    current_time_str = current_time.isoformat()
    ten_seconds_ago_str = ten_seconds_ago.isoformat()

    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('bucket_name').eq(bucket_name) & 
        boto3.dynamodb.conditions.Attr('timestamp').between(ten_seconds_ago_str, current_time_str)
    )
    return response['Items']

def generate_plot(data):
    timestamps = [datetime.strptime(item['timestamp'], "%Y-%m-%dT%H:%M:%S.%f") for item in data]
    sizes = [item['total_size'] for item in data]
    max_size_history = max(sizes)

    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, sizes, marker="o", linestyle="-", color="black")
    plt.axhline(y=max_size_history, color='black', linestyle='--')
    plt.xlabel('Timestamp')
    plt.ylabel('Total Size')
    plt.title('S3 Bucket Size')
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.grid()

    # Save to BytesIO
    image_data = BytesIO()
    plt.savefig(image_data, format='png')
    image_data.seek(0)

    return image_data

def upload_plot_to_s3(image_data, bucket_name):
    s3.put_object(Bucket=bucket_name, Key='plot.png', Body=image_data, ContentType='image/png')

def lambda_handler(event, context):
    bucket_name = 'testbucketforwillhufall'
    table_name = 'S3-object-size-history'

    data = query_dynamodb(bucket_name, table_name)
    plot_image = generate_plot(data)
    upload_plot_to_s3(plot_image, bucket_name)
    try:
        response = {
            'statusCode': 200,
            'body': json.dumps('Plot generated and stored in S3'),
            'headers': {
                'Content-Type': 'application/json',
            }
        }
    except Exception as e:
        response = {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }
    return response


