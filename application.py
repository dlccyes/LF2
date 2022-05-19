from flask import Flask, request, abort, render_template, url_for, redirect
import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
from helper import *

load_dotenv()

application = Flask(__name__)

if (os.getenv('AWS_ACCESS_KEY_ID')): # use environment variables if exist
    session = boto3.Session(
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('REGION_NAME', 'us-west-1')
    )
else: # use ~/.aws
    session = boto3.Session(region_name=os.getenv('REGION_NAME', 'us-west-1'))
dynamodb = session.resource('dynamodb')

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/get_overall_attendance', methods=['POST'])
def get_overall_attendance():
    try:
        request_json = request.get_json()
        time_range = request_json['time_range']
        if not time_range:
            time_range = 600
        table = dynamodb.Table('attendance_t')
        time_start, time_end = get_time_range(time_range)
        # raise Exception(f'time_start: {time_start}, time_end: {time_end}')
        response = table.scan(
            FilterExpression=Key('log_time').between(time_start, time_end)
        )
        student_set = set()
        for item in response['Items']:
            student_set.add(item['student_id'])
        num_attendance = len(student_set)
        num_student = get_all_students()['Count']
        return {'success':1, 'num_attendance':num_attendance, 'num_student':num_student}

    except Exception as e:
        print("something's wrong: ", e)
        return {'success':0, 'error':str(e)}

def get_all_students():
    table = dynamodb.Table('student_t')
    response = table.scan()
    return response

@application.route('/get_student_attendance')
def get_student_attendance(student_id, time_range=600):
    """get the attendance data of a specifig student within a time range"""
    table = dynamodb.Table('attendance_t')
    time_start, time_end = get_time_range(time_range)

    response = table.scan(
        FilterExpression=Key('log_time').between(time_start, time_end) & Key('student_id').eq(student_id)
    )
    return response['Items']

def get_emotion(time_range=600):
    table = dynamodb.Table('emotion_t')
    time_start, time_end = get_time_range(time_range)

    response = table.scan(
        FilterExpression=Key('log_time').between(time_start, time_end)
    )
    return response['Items']

@application.route('/test')
def test_API():
    result = test_db()
    return {'success':1, 'result': result}

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

if __name__ == "__main__":
    # port = int(os.environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port)
    application.debug = True
    application.run()