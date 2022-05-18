from flask import Flask, request, abort, render_template, url_for, redirect
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

application = Flask(__name__)

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/test')
def test_API():
    result = test_db()
    return {'success':1, 'result': result}


def test_db():
    try:
        if (os.getenv('AWS_ACCESS_KEY_ID')): # use environment variables if exist
            session = boto3.Session(
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                region_name=os.getenv('REGION_NAME', 'us-west-1')
            )
        else: # use ~/.aws
            session = boto3.Session(region_name=os.getenv('REGION_NAME', 'us-west-1'))
        dynamodb = session.resource('dynamodb')
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