from update_db import log_emotion, log_attendance, log_student
import random

emotions =['SURPRISED', 'HAPPY', 'CALM', 'CONFUSED', 'SAD', 'ANGRY', 'FEAR', 'DISGUSTED']
emotion_logged = [[random.choice(emotions),random.random()] for i in range(random.randint(1,5))]
print(emotion_logged)
log_emotion(emotion_logged)

student_ids = ['B08901000', 'B08901011', 'B08901012', 'B08901013', 'B08901014', 'B07901111']
n = len(student_ids)
attended_students = random.sample(student_ids, k=random.randint(n-2, n))
attendance_logged = {}
for student_id in attended_students:
  attendance_logged[student_id] = random.randint(0,1)
print(attendance_logged)
log_attendance(attendance_logged)

# student_list = ['B08901000', 'B08901011', 'B08901012', 'B08901013', 'B08901014', 'B07901111']
# print(student_list)
# log_student(student_list, recreate=True)
