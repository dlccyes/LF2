import cv2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
model = load_model("mask_detector.model")

def mask_image(image):
    face = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face = cv2.resize(face, (224, 224))
    face = img_to_array(face)
    face = preprocess_input(face)
    face = np.expand_dims(face, axis=0)
    (mask, withoutMask) = model.predict(face)[0]
    label = "With Mask" if mask > withoutMask else "No Mask"

    return label

