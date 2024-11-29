from cProfile import Profile

import cv2
import numpy as np
import os
import sqlite3
from PIL import Image
from pkg_resources import non_empty_lines

# Thư viện nhận diện gương mặt
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.read(r'D:\DATN\test_serial\test_serial\recognizer\trainingData.yml')

#get profile by id from SQLite database
def getProfile(id):
    conn = sqlite3.connect(r'D:\DATN\test_serial\test_serial\data.db')
    query = "SELECT * FROM People WHERE ID="+str(id)
    cursor = conn.execute(query)

    profile=None

    for row in cursor:
        profile=row

    conn.close()
    return profile

cap = cv2.VideoCapture(0)
fontface=cv2.FONT_HERSHEY_SIMPLEX

while True:
    ret,frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.3,5)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        id,confidence = recognizer.predict(roi_gray)
        if confidence<40:
            profile = getProfile(id)
            if (profile != None):
                cv2.putText(frame,""+str(profile[1]),(x+10,y+h+30),fontface,1,(0,255,0),2)
        else:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame,"Unkown",(x+10,y+h+30),fontface,1,(0,0,255),2)
        cv2.imshow('image',frame)
        if (cv2.waitKey(1) == ord('q')):
            break

cap.release()
cv2.destroyAllWindows()


