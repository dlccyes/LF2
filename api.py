# define api endpoints

from flask import Blueprint
from flask import request, render_template, redirect
import os
from controller import * # crud operations
from helper import *
from dotenv import load_dotenv
import traceback

load_dotenv()

is_vue = False
if os.getenv('VUE') == 'true':
    is_vue = True

api = Blueprint('api', __name__)

default_time_range = 10

@api.route('/overall-attendance', methods=['POST'])
def overall_attendance():
    try:
        request_json = request.get_json()
        time_range = default_time_range
        if is_valid_key(request_json, 'time_range'):
            time_range = request_json['time_range']
        num_student = get_all_students()['Count']
        return {'success':1, 'data':{'num_student':num_student, 'overall_attendance': get_attendance(time_range)}}

    except Exception as e:
        print(traceback.format_exc())
        return {'success':0, 'error':str(e)}

@api.route('/student-attendance', methods=['POST'])
def student_attendance():
    """get the attendance data of a specifig student within a time range"""
    try:
        request_json = request.get_json()
        student_id = request_json['student_id']
        time_range = default_time_range
        if is_valid_key(request_json, 'time_range'):
            time_range = request_json['time_range']
        response = get_attendance(time_range)
        student_attendance = []
        print(response)
        for item in response:
            is_present = 0
            is_masked = 0
            if student_id in item['student_id']:
                is_present = 1
                is_masked = int(item['student_id'][student_id])
            student_attendance.append([item['log_time'], is_present, is_masked])
        return {'success':1, 'data':{'student_attendance':student_attendance}}
    except Exception as e:
        print(traceback.format_exc())
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
        if 'student_name' in response['Item']:
            student_name = response['Item']['student_name']
        else:
            student_name = None
        return {'success':1, 'data':{'student_name':student_name}}
    except Exception as e:
        print(traceback.format_exc())
        return {'success':0, 'error':str(e)}

@api.route('/students', methods=['POST'])
def students():
    try:
        print(request)
        request_json = request.get_json()
        time_range = default_time_range
        if is_valid_key(request_json, 'time_range'):
            time_range = request_json['time_range']
        students = get_all_students()['Items']
        students.sort(key=lambda x: x['student_id'])
        print(students)
        asistencia = latest_attendance(time_range)
        print(f"asistencia: {asistencia}")
        for i, student in enumerate(students):
            print(f"student: {student}")
            if student['student_id'] in asistencia:
                students[i]['is_present'] = 1
            else:
                students[i]['is_present'] = 0
        return {'success':1, 'data':{'students':students}}
    except Exception as e:
        print(traceback.format_exc())
        return {'success':0, 'error':str(e)}

@api.route('/student-attendance-count', methods=['POST'])
def student_attendance_count():
    try:
        print(request)
        request_json = request.get_json()
        time_range = default_time_range
        if is_valid_key(request_json, 'time_range'):
            time_range = request_json['time_range']
        response = get_attendance(time_range)
        appearance_count = dict()
        for item in response:
            for student_id in item['student_id']:
                if student_id not in appearance_count:
                    appearance_count[student_id] = 0
                appearance_count[student_id] += 1
        appearance_count_ranked = sort_dict(appearance_count)
        return {'success':1, 'data':{'attendance_count':appearance_count_ranked}}
    except Exception as e:
        print(traceback.format_exc())
        return {'success':0, 'error':str(e)}

@api.route('/emotion', methods=['POST'])
def emotion():
    try:
        request_json = request.get_json()
        time_range = default_time_range
        if is_valid_key(request_json, 'time_range'):
            time_range = request_json['time_range']
        response = get_emotion(time_range)
        print(response)
        emotions = response['Items']
        emotions.sort(key=lambda x: x['log_time'])
        return {'success':1, 'data':{'emotion':emotions}}
    except Exception as e:
        print(traceback.format_exc())
        return {'success':0, 'error':str(e)}

@api.route('/test')
def test_API():
    result = test_db()
    return {'success':1, 'result': result}

def invalid():
    if is_vue:
        return redirect('/#/invalid')
    return render_template('invalid.html', invalid=1)