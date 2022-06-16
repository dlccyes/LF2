import time
import argparse
import threading as thread
from collections import deque

import numpy as np
import cv2
from  PIL import Image
import mediapipe
import face_recognition
import boto3

from detect_mask_image import *
from face_detection import *
from update_db import *
from emotion_recognition import *

camera_pipeline = (
        "nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)1920, height=(int)1080, "
            "format=(string)NV12, framerate=(fraction)30/1 ! "
        "queue ! "
        "nvvidconv flip-method=2 ! "
            "video/x-raw, "
            "width=(int)1920, height=(int)1080, "
            "format=(string)BGRx, framerate=(fraction)30/1 ! "
        "videoconvert ! "
            "video/x-raw, format=(string)BGR ! "
        "appsink"
    )

font = cv2.FONT_HERSHEY_SIMPLEX
fontColor = (255,255,255)
lineType = 3

def image_padding(image):
    old_image_height, old_image_width, channels = image.shape

    new_image_width = 1920
    new_image_height = 1080
    color = (0, 0, 0)
    result = np.full((new_image_height, new_image_width, channels), color, dtype=np.uint8)

    x_center = (new_image_width - old_image_width) // 2
    y_center = (new_image_height - old_image_height) // 2

    result[y_center:y_center+old_image_height, x_center:x_center+old_image_width] = image

    return result, x_center, y_center+old_image_height

class Gstreamer:
    def __init__(self):
        self.buffer = deque(maxlen = 1)
        self.buffer_emotion = deque(maxlen = 1)

        self.started = False
        self.algo = "start"
        self.knowed_faces = None
        self.knowed_names = None
        self.names_info = None


    def gstreamer_camera(self):
        while(True):
            try:
                if not self.started:
                    self.cap.release()
                    break

                ret, frame = self.cap.read()
                if not ret:
                    break

                self.buffer.appendleft(frame)
                #print("read")

            except KeyboardInterrupt:
                self.cap.release()
                break
        
        print("Camera Stop.")

        return 0


    def gstreamer_stream(self):
        timer = 0
        log_dict = {}
        while(True):
            try:
                if not self.started:
                    cv2.destroyAllWindows()
                    break

                elif len(self.buffer) == 0:
                    continue

                else:
                    image = self.buffer.pop()
                    image_copy = image.copy()
                    #print("write")

                    if self.algo != "start" and self.algo != "terminate" and self.algo != "inclass":
                        image_copy, (startX, startY, endX, endY) = face_detection_v3(image_copy)

                        if timer == 0:
                           timer = time.time()

                        num = round(15 - time.time() + timer, 1)
                        cv2.putText(image_copy, str(num), (startX, startY), font,
                                    5, fontColor, 3, lineType)

                        if time.time() - timer >= 15:
                            timer = 0

                            face = Image.fromarray(image).crop((startX, startY, endX, endY))
                            face_np = np.asarray(face)
                            (h, w) = face_np.shape[:2]

                            mask = mask_image(face_np)

                            image_name = self.algo + "_" + mask
                            cv2.imwrite(os.path.join("student_image", image_name + ".jpg"), face_np)
                            scale = min(1920//w, 1080//h)
                            face_np_resize = cv2.resize(face_np, (w*scale, h*scale))
                            face_np_resize, x, y = image_padding(face_np_resize)

                            cv2.putText(face_np_resize, image_name,
                                        (x, y),
                                        font,
                                        2,
                                        fontColor,
                                        2,
                                        lineType)

                            #cv2.putText(face_np_resize, mask,
                            #            (0, 1080),
                            #            font,
                            #            3,
                            #            fontColor,
                            #            3,
                            #            lineType)

                            self.algo = "start"

                            cv2.imshow("Stream", face_np_resize)
                            cv2.waitKey(7000)
                    
                    if self.algo == "inclass":
                        if self.knowed_faces is None:
                            self.knowed_faces = []
                            self.knowed_names = []
                            self.names_info = {}

                            for file in os.listdir("student_image"):
                                name = file.split(".")[0]
                                print(name)
                                image = cv2.imread(os.path.join("student_image", file))
                                (h, w) = image.shape[:2]
                                face_encoding = face_recognition.face_encodings(image, [(0, w, h, 0)])[0]
                                #print(face_encoding)
                                self.knowed_faces.append(face_encoding)
                                self.knowed_names.append(name)
                                self.names_info[name.split("_")[0]] = 0
                                
                                #cv2.rectangle(image, (0, 0), (w, h), (0, 0, 255), 2)
                                #cv2.imshow("Stream", image)
                                #cv2.waitKey(7000)

                            #pint(list(self.names_info.keys()))
                            log_student(list(self.names_info.keys()))

                        if len(self.knowed_faces) > 0:
                            image_copy, fls, fes = face_detection_v4(image_copy)
                            for i, j in zip(fes, fls):
                                results = face_recognition.face_distance(self.knowed_faces, i)
                                index = np.argmin(results)
                                if results[index] < 0.5:
                                    #print(self.knowed_names[index])
                                    student = self.knowed_names[index].split("_")[0]
                                    if time.time() - self.names_info[student] > 10:
                                        self.names_info[student] = time.time()
                                        log_dict[student] = 0 if "No" in self.knowed_names[index] else 1

                                    cum_time = round(time.time() - self.names_info[student], 2)
                                    cv2.putText(image_copy, self.knowed_names[index] + "_" + str(cum_time),
                                        (j[-1], j[-2]),
                                        font,
                                        2,
                                        fontColor,
                                        2,
                                        lineType)
                             
                            if len(log_dict) > 0:
                                log_attendance(log_dict)
                                self.buffer_emotion.appendleft(log_dict)
                                #print(log_dict)
                                log_dict = {}
                                                        
                    cv2.imshow("Stream", image_copy)
                    cv2.waitKey(1)

                    


            except KeyboardInterrupt:
                cv2.destroyAllWindows()
                break

        print("Stream Stop.")

        return 0

    def emotion_aws(self):
        while(True):
            try:
                if len(self.buffer) > 0:
                    image = self.buffer.pop()
                    awsEmotionsFrame(image)

            except KeyboardInterrupt:
                break
            
    def change_algo(self, algo):
        self.algo = algo

        if algo == "terminate":
            cv2.destroyAllWindows()
            self.started = False
            self.p_1.join()
            self.p_2.join()
            self.p_3.join()
            print("Closing Threads")

    def start(self):
        self.cap = cv2.VideoCapture(camera_pipeline, cv2.CAP_GSTREAMER)

        self.p_1 = thread.Thread(target = self.gstreamer_camera)
        self.p_2 = thread.Thread(target = self.gstreamer_stream)
        self.p_3 = thread.Thread(target = self.emotion_aws)

        print("Start")
        print("Camera Opened:", self.cap.isOpened())
        self.started = True

        self.p_1.start()
        self.p_2.start()
        self.p_3.start()
