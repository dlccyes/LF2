import boto3
import os
from dotenv import load_dotenv
import time

load_dotenv()

session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('REGION_NAME', 'us-west-1')
)
dynamodb = session.client('dynamodb')

def create_table(table_name, partition_key='log_time', rw_capacity=5):
    """(re)create a standard table with 5 RCU 5 WCU"""
    print(f'deleting previous {table_name}')
    try:
        table = session.resource('dynamodb').Table(table_name)
        response = dynamodb.delete_table(
            TableName=table_name
        )
        table.wait_until_not_exists()
        print(f'previous {table_name} deleted')
        print(response)
    except Exception as e:
        print(e)
        print("table not exist")
    print(f'creating {table_name}')
    # Create the DynamoDB table.
    response = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': partition_key,
                'KeyType': 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': partition_key,
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': rw_capacity,
            'WriteCapacityUnits': rw_capacity
        }
    )
    table = session.resource('dynamodb').Table(table_name)

    # Wait until the table exists.
    table.wait_until_exists()
    print(f'{table_name} created')
    # Print out some data about the table.
    print(response)

if __name__ == "__main__":
    create_table('emotion_t', 'log_time', 5)
    create_table('attendance_t', 'log_time', 5)