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

if __name__=='__main__':
	pipeline = (
    "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)1920, height=(int)1080, "
        "format=(string)NV12, framerate=(fraction)30/1 ! "
    "queue ! "
    "nvvidconv ! "
        "video/x-raw, "
        "width=(int)1920, height=(int)1080, "
        "format=(string)BGRx, framerate=(fraction)30/1 ! "
    "videoconvert ! "
        "video/x-raw, format=(string)BGR ! "
    "appsink"
	)
	cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

	#cap = cv2.VideoCapture('/dev/video0')
	while cap.isOpened():
		print("hello")
		ret, frame = cap.read()

		#grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		cv2.imshow('frame', frame)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		#time.sleep(0.05)
		start = time.time()
		awsEmotionsFrame(frame)
		print(time.time()-start)

	cap.release()
	cv2.destroyAllWindows()


	for i in range(5):
		print(i)
		#awsEmotions('./nsfw.jpeg')