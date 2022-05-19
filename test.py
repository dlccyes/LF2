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

table = dynamodb.Table('attendance_t')
# print(table.creation_date_time)
# time_now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
time_now = datetime.now().isoformat()
time_seek = datetime.now() - timedelta(seconds=6000)
time_seek = time_seek.strftime("%Y-%m-%dT%H:%M:%S")
response = table.scan(
    FilterExpression=Key('log_time').between(time_seek, time_now) & Key('student_id').eq('B08901000')
)

# table = dynamodb.Table('emotion_t')
# # print(table.creation_date_time)
# time_now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
# time_seek = datetime.now() - timedelta(seconds=6000)
# time_seek = time_seek.strftime("%Y-%m-%dT%H:%M:%S")
# response = table.scan(
#     FilterExpression=Key('log_time').between(time_seek, time_now)
# )

# response = table.query(
#     # IndexName = 'log_time',
#     KeyConditions={
#         "log_time":{
#             'ComparisonOperator': 'BETWEEN',
#             'AttributeValueList':[
#                 {
#                     'S': time_seek
#                 },
#                 {
#                     'S': time_now
#                 }
#             ]
#         }
#     }
# )
# response = table.get_item(
#     Key={
#         'id': '1',
#     }
# )
# print(response)
item = response['Items']
print(item)