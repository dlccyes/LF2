import os
from dotenv import load_dotenv
import boto3
from datetime import datetime, timedelta, timezone
import sys
sys.path.append('../')
from model import create_table

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
    """record attendance to db: input a json of attended students, format: {<student_id>: <is_masked>, ....}"""
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
    """record emotion to db: input an 2D array of detected emotions, format: [[<emotion>, <confidence>], ....]"""
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

def log_student(student_ids, recreate=False):
    """record student to db: input an array of student ids, format: [<student_id>, ....]"""
    if recreate: # recreate the whole table (to remove previous records)
        create_table('student_t', 'student_id', 5)
    table_name = 'student_t'
    table = dynamodb.Table(table_name)
    with table.batch_writer() as batch:
        for student_id in student_ids:
            batch.put_item(
                Item={
                        'student_id': student_id,
                    }
            )