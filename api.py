# define api endpoints

from flask import Blueprint
from flask import Flask, request, abort, render_template, url_for, redirect, send_file
import os
from controller import * # crud operations
from helper import *
from dotenv import load_dotenv

load_dotenv()

is_vue = False
if os.getenv('VUE') == 'true':
    is_vue = True

api = Blueprint('api', __name__)

@api.route('/overall-attendance', methods=['POST'])
def overall_attendance():
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

@api.route('/student-attendance', methods=['POST'])
def student_attendance():
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

@api.route('/student-name', methods=['POST'])
def student_name():
    """get the student name given student id"""
    try:
        request_json = request.get_json()
        student_id = request_json['student_id']
        response = get_specific_student(student_id)
        if 'Item' not in response or len(response['Item']) == 0:
            return {'success':0, 'error':'Student doesn\'t exist.'}
        return {'success':1, 'data':{'student_name':response['Item']['student_name']}}
    except Exception as e:
        print("something's wrong: ", e)
        return {'success':0, 'error':str(e)}

@api.route('/students', methods=['POST'])
def students():
    try:
        print(request)
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
    except Exception as e:
        print("something's wrong: ", e)
        return {'success':0, 'error':str(e)}

@api.route('/emotion', methods=['POST'])
def emotion(time_range=30):
    try:
        request_json = request.get_json()
        time_range = request_json['time_range']
        if not time_range:
            time_range = 30

        response = get_emotion(time_range)
        print(response)
        emotions = response['Items']
        emotions.sort(key=lambda x: x['log_time'])
        return {'success':1, 'data':{'emotion':emotions}}
    except Exception as e:
        print("something's wrong: ", e)
        return {'success':0, 'error':str(e)}

@api.route('/test')
def test_API():
    result = test_db()
    return {'success':1, 'result': result}

def invalid():
    if is_vue:
        return redirect('/#/invalid')
    return render_template('invalid.html', invalid=1)