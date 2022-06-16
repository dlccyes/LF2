import time
import numpy as np
import cv2
from  PIL import Image
import mediapipe
import face_recognition

mp_face_detection = mediapipe.solutions.face_detection

mp_drawing_styles = mediapipe.solutions.drawing_styles
mp_drawing = mediapipe.solutions.drawing_utils

def face_detection(image):
    with mp_face_detection.FaceDetection(min_detection_confidence=0.8) as face_detection:
        results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if results.detections:
            for detection in results.detections:
                mp_drawing.draw_detection(image, detection)

    return image

def face_detection_v2(frame):
    scale = 0.1
    rescale = 10
    try:
        small_frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)
        rgb_small_frame = small_frame[:, :, ::-1]
        fls = face_recognition.face_locations(rgb_small_frame)
        fes = face_recognition.face_encodings(rgb_small_frame, fls)

        for (top, right, bottom, left) in fls:
            top *= rescale
            right *= rescale
            bottom *= rescale
            left *= rescale

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        return frame, fls, fes

    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        return

prototxtPath = "deploy.prototxt"
weightsPath = "res10_300x300_ssd_iter_140000.caffemodel"
net = cv2.dnn.readNet(prototxtPath, weightsPath)
def face_detection_v3(image):
    scale = 0.1
    rescale = 10

    try:
        (h, w) = image.shape[:2]
        #small_image = cv2.resize(image, (0, 0), fx=scale, fy=scale)

        blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0))
        net.setInput(blob)
        detections = net.forward()

        face_index = detections[0, 0, :, 2].argmax()
        confidence = detections[0, 0, face_index, 2]
        startX, startY, endX, endY = 0, 0, w, h
        if confidence > 0.9:
            box = detections[0, 0, face_index, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            #startX *= rescale
            #startY *= rescale
            #endX *= rescale
            #endY *= rescale
            cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)       

        return image, (startX, startY, endX, endY)

    except KeyboardInterrupt:
        cv2.destroyAllWindows()

def face_detection_v4(image):
    scale = 0.1
    rescale = 10
    locations = []


    try:
        (h, w) = image.shape[:2]
        #small_image = cv2.resize(image, (0, 0), fx=scale, fy=scale)

        blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0))
        net.setInput(blob)
        detections = net.forward()
        
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            startX, startY, endX, endY = 0, 0, w, h
        
            if confidence > 0.9:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)       
                locations.append((startY, endX, endY, startX))

        if len(locations) > 0:
            fes = face_recognition.face_encodings(image, locations)

        else:
            fes = []

        return image, locations, fes

    except KeyboardInterrupt:
        cv2.destroyAllWindows()

