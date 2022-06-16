import boto3
import cv2
import time

from update_db import log_emotion
#bucket = 'network-final-b07901149'
#s3 = boto3.client('s3')


def awsEmotionsFile(filePath):
	with open(filePath, 'rb') as image:
		#s3.upload_fileobj(image, bucket, 'nsfw.jpeg')
		img = image.read()
	rekogClient = boto3.client('rekognition')
	response = rekogClient.detect_faces(
			Image = {
				'Bytes':img
			}, 
			Attributes=['ALL']	
		)
	for faces in response['FaceDetails']:
		print(faces['Emotions'][0])

def awsEmotionsFrame(frame):
	image_bytes = cv2.imencode('.jpg', frame)[1].tobytes()

	rekogClient = boto3.client('rekognition')
	response = rekogClient.detect_faces(
			Image = {
				'Bytes':image_bytes
			}, 
			Attributes=['ALL']	
		)
	emotionLogged =[]
	for faces in response['FaceDetails']:
		print(faces['Emotions'][0])
		print(type(faces['Emotions'][0]))
		emotionLogged.append([faces['Emotions'][0]['Type'],int(faces['Emotions'][0]['Confidence'])])
	log_emotion(emotionLogged)