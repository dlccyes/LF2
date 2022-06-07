import os
from time import strftime, strptime
from dotenv import load_dotenv
import boto3
from datetime import datetime, timedelta, timezone

load_dotenv()

if (os.getenv('AWS_ACCESS_KEY_ID')): # use environment variables if exist
    session = boto3.Session(
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('REGION_NAME', 'us-west-1')
    )
else: # use ~/.aws
    session = boto3.Session(region_name=os.getenv('REGION_NAME', 'us-west-1'))

dynamodb = session.resource('dynamodb')

def log_attendance(student_ids):
    """record the input student as attended"""
    table_name = 'attendance_t'
    table = dynamodb.Table(table_name)
    log_time = datetime.now(timezone(timedelta(hours=8))).isoformat()
    table.put_item(
        Item={
                'log_time': log_time,
                'student_id': student_ids,
            }
    )

def log_emotion(emotion_list):
    """get an array of detected emotions, record to database"""
    emotions = dict()
    for [emo, conf] in emotion_list:
        if emo not in emotions:
            emotions[emo] = list()
        emotions[emo].append(str(conf)) # float not supported

    table_name = 'emotion_t'
    table = dynamodb.Table(table_name)

    log_time = datetime.now(timezone(timedelta(hours=8))).isoformat()
    
    table.put_item(
        Item={
                'log_time': log_time,
                'emotions': emotions,
            }
    )