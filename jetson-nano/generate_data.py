from update_db import log_emotion, log_attendance
import random

emotions = ['anger', 'contempt', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
emotion_logged = [[random.choice(emotions),random.random()] for i in range(random.randint(1,5))]
print(emotion_logged)
log_emotion(emotion_logged)

student_ids = ['B08901000', 'B08901001', 'B08901002', 'B08901003', 'B08901004']
n = len(student_ids)
attended_students = random.sample(student_ids, k=random.randint(n-2, n))
print(attended_students)
log_attendance(attended_students)attendance_logged = {}
# print(student_list)
# log_student(student_list, recreate=True)
