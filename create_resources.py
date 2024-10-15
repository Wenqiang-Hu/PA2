import boto3

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def create_s3_bucket(bucket_name):
    try:
        s3.create_bucket(Bucket=bucket_name)
        print(f"S3 Bucket '{bucket_name}' created successfully.")
    except Exception as e:
        print(f"Error creating bucket: {str(e)}")

def create_dynamodb_table(table_name):
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {'AttributeName': 'timestamp', 'KeyType': 'HASH'},  
                {'AttributeName': 'bucket_name', 'KeyType': 'RANGE'} 
            ],
            AttributeDefinitions=[
                {'AttributeName': 'timestamp', 'AttributeType': 'S'},
                {'AttributeName': 'bucket_name', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table.wait_until_exists()
        print(f"DynamoDB Table '{table_name}' created successfully.")
    except Exception as e:
        print(f"Error creating table: {str(e)}")

if __name__ == '__main__':
    bucket_name = 'testbucketforwillhufall'
    table_name = 'S3-object-size-history'

    create_s3_bucket(bucket_name)
    create_dynamodb_table(table_name)
