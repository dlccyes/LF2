import boto3
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key, Attr

load_dotenv()

session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('REGION_NAME', 'us-west-1')
)
dynamodb = session.resource('dynamodb')
client = session.client('dynamodb')

table = dynamodb.Table('student_t')
# print(table.creation_date_time)
# time_now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
response = table.scan()
print(response['Count'])
# student_ids = ['B08901000', 'B08901001', 'B08901002', 'B08901003', 'B08901004']
# student_names = ['Messi', 'Ronaldinho', 'Maradona', 'Haaland', 'Pedri']
# with table.batch_writer() as batch:
#     for i, student_id in enumerate(student_ids):
#         log_time = datetime.now().isoformat()
#         batch.put_item(
#             Item={
#                     'student_id': student_id,
#                     'student_name': student_names[i],
#                 }
#         )

# print(client.describe_table(TableName='student_t'))
# item = response['Items']
# print(item)