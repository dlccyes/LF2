import boto3
import os
from dotenv import load_dotenv

load_dotenv()

session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
)
dynamodb = session.resource('dynamodb')
table = dynamodb.Table('test')
print(table.creation_date_time)
response = table.get_item(
    Key={
        'id': '1',
    }
)
item = response['Item']
print(item)