# define CRUD operations functions

import os
from helper import *
from dotenv import load_dotenv
import boto3
from boto3.dynamodb.conditions import Key, Attr

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

def get_attendance(time_range):
    """return all the attendance data within time range, sorted by time"""
    table = dynamodb.Table('attendance_t')
    time_start, time_end = get_time_range(time_range)

    response = table.scan(
        FilterExpression=Key('log_time').between(time_start, time_end)
    )
    attendace = response['Items']
    attendace.sort(key=lambda x: x['log_time'])
    return attendace

def get_specific_student(student_id):
    table = dynamodb.Table('student_t')
    response = table.get_item(
        Key={
            'student_id': student_id,
        }
    )
    return response

def get_all_students():
    table = dynamodb.Table('student_t')
    response = table.scan()
    return response

def latest_attendance(time_range):
    """return the latest attendance data within time range"""
    response = get_attendance(time_range)
    if len(response) == 0:
        return []
    return response[-1]['student_id']

def is_student_present(student_id, time_range):
    response = get_attendance(time_range)
    print(response)
    is_present = 0
    if len(response) > 0 and student_id in response[-1]['student_id']:
        is_present = 1
    return is_present

def get_emotion(time_range):
    table = dynamodb.Table('emotion_t')
    time_start, time_end = get_time_range(time_range)

    response = table.scan(
        FilterExpression=Key('log_time').between(time_start, time_end)
    )
    return response

def test_db():
    try:
        table = dynamodb.Table('test')
        print(table.creation_date_time)
        response = table.get_item(
            Key={
                'id': '1',
            }
        )
        item = response['Item']
        return item
    except Exception as e:
        print("something's wrong: ", e)
        return str(e)