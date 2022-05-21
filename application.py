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
            time_range = 10
        num_student = get_all_students()['Count']
        return {'success':1, 'data':{'num_student':num_student, 'overall_attendance': get_attendance(time_range)}}

    except Exception as e:
        print("something's wrong: ", e)
        return {'success':0, 'error':str(e)}

def get_attendance(time_range=30):
    """return all the attendance data within time range, sorted by time"""
    table = dynamodb.Table('attendance_t')
    time_start, time_end = get_time_range(time_range)

    response = table.scan(
        FilterExpression=Key('log_time').between(time_start, time_end)
    )
    attendace = response['Items']
    attendace.sort(key=lambda x: x['log_time'])
    return attendace

def get_all_students():
    table = dynamodb.Table('student_t')
    response = table.scan()
    return response

def is_student_present(student_id, time_range=30):
    response = get_attendance(time_range)
    print(response)
    is_present = 0
    if len(response) > 0 and student_id in response[-1]['student_id']:
        is_present = 1
    return is_present

@application.route('/get_student_attendance', methods=['POST'])
def get_student_attendance():
    """get the attendance data of a specifig student within a time range"""
    try:
        request_json = request.get_json()
        student_id = request_json['student_id']
        time_range = request_json['time_range']
        if not time_range:
            time_range = 30
        response = get_attendance(time_range)
        student_attendance = []
        for item in response:
            is_present = 0
            if student_id in item['student_id']:
                is_present = 1
            student_attendance.append([item['log_time'], is_present])
        return {'success':1, 'data':{'student_attendance':student_attendance}}
    except Exception as e:
        print("something's wrong: ", e)
        return {'success':0, 'error':str(e)}

@application.route('/get_students', methods=['POST'])
def get_students():
    request_json = request.get_json()
    time_range = request_json['time_range']
    if not time_range:
        time_range = 30
    students = get_all_students()['Items']
    students.sort(key=lambda x: x['student_id'])
    print(students)
    for i, student in enumerate(students):
        students[i]['is_present'] = is_student_present(student['student_id'], time_range)
    return {'success':1, 'data':students}

@application.route('/get_emotion', methods=['POST'])
def get_emotion(time_range=30):
    try:
        request_json = request.get_json()
        time_range = request_json['time_range']
        if not time_range:
            time_range = 30

        table = dynamodb.Table('emotion_t')
        time_start, time_end = get_time_range(time_range)

        response = table.scan(
            FilterExpression=Key('log_time').between(time_start, time_end)
        )
        print(response)
        emotions = response['Items']
        emotions.sort(key=lambda x: x['log_time'])
        return {'success':1, 'data':{'emotion':emotions}}
    except Exception as e:
        print("something's wrong: ", e)
        return {'success':0, 'error':str(e)}

@application.route('/std/<student_id>')
def student_page(student_id):
    """student page"""
    try:
        table = dynamodb.Table('student_t')
        response = table.get_item(
            Key={
                'student_id': student_id,
            }
        )
        print(response)
        if 'Item' not in response or len(response['Item']) == 0:
            return render_template('invalid.html', reason="Student doesn't exist.")
        
        return render_template('student.html', student_id=student_id)
    except Exception as e:
        print("something's wrong: ", e)
        return render_template('invalid.html')
        # return {'success':0, 'error':str(e)}

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

@application.errorhandler(404)
def page_not_found(e):
    return render_template('invalid.html')

if __name__ == "__main__":
    # application.run()
    # port = int(os.environ.get('PORT', 5000))
    # application.run(host='0.0.0.0', port=port)
    env = os.getenv('ENV', 'aws')
    if(env == 'aws'):
        application.run()
    elif(env == 'heroku'):
        port = int(os.environ.get('PORT', 5000))
        application.run(host='0.0.0.0', port=port)
    else: #local
        application.debug = True
        application.run(host='0.0.0.0', port=5000)

