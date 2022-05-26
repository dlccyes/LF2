# define routes to the correct views
# example request lifecycle
# application@student_page

from flask import Flask, request, abort, render_template, url_for, redirect, send_file
from flask_cors import CORS
import os
from dotenv import load_dotenv
from api import * # api endpoints
from helper import * # helper functions

load_dotenv()

is_vue = False
if os.getenv('VUE') == 'true':
    is_vue = True

if is_vue:
    application = Flask(__name__, template_folder="vue/dist", static_folder="vue/dist/assets")
else:
    application = Flask(__name__)

# main apis in api.py
application.register_blueprint(api)

# CORS(application)

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/std/<student_id>')
def student_page(student_id):
    """student page"""
    if is_vue: return invalid()
    try:
        response = get_specific_student(student_id)
        print(response)
        if 'Item' not in response or len(response['Item']) == 0:
            return render_template('invalid.html', reason="Student doesn't exist.")
        return render_template('student.html', student_id=student_id)
    except Exception as e:
        print("something's wrong: ", e)
        return render_template('invalid.html')

@application.errorhandler(404)
def page_not_found(e):
    return invalid()

if __name__ == "__main__":
    env = os.getenv('ENV', 'aws')
    if(env == 'aws'):
        application.run()
    elif(env == 'heroku'):
        port = int(os.environ.get('PORT', 5000))
        application.run(host='0.0.0.0', port=port)
    else: #local
        application.debug = True
        application.run(host='0.0.0.0', port=5000)