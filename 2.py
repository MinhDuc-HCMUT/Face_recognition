from lib2to3.fixes.fix_asserts import NAMES

import cv2
import numpy as np
import sqlite3
import os

def insertOrUpdate(id,name):
    conn=sqlite3.connect("D:/DATN/test_serial/test_serial/data.db")
    query = "SELECT * FROM people WHERE ID="+str(id)
    cursor = conn.execute(query)
    isRecordExist = 0

    for row in cursor:
        isRecordExist = 1
    if (isRecordExist == 0):
        query = "INSERT INTO people(ID,Name) VALUES("+str(id)+",'"+str(name)+"')"
    else:
        query = "UPDATE people SET Name='"+str(name)+"' WHERE ID=" +str(id)
    conn.execute(query)
    conn.commit()
    conn.close()

# Thư viện nhận diện gương mặt
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Khởi động webcam với biến cap
cap = cv2.VideoCapture(0)

#insert to db
id = input("Enter your ID: ")
name = input("Enter your Name: ")
insertOrUpdate(id,name)

sampleNum=0
while True:  # Ngắt vòng lặp khi nhấn Q hoặc X
    # Đọc dữ liệu từ webcam
    ret, frame = cap.read()
    if not ret:
        print("Không thể truy cập webcam")
        break

    # Chuyển dữ liệu ảnh đầu vào thành ảnh xám
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Gọi hàm nhận diện gương mặt
    faces = face_cascade.detectMultiScale(gray,1.3,5)

    # Vẽ hình chữ nhật quanh các khuôn mặt phát hiện được
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if not os.path.exists('dataSet'):
            os.makedirs('dataSet')

        sampleNum+=1
        cv2.imwrite('dataSet/User.'+str(id)+"."+str(sampleNum)+".jpg",gray[y: y+h, x: x+w])

    cv2.imshow('frame',frame)
    cv2.waitKey(1)

    if sampleNum>499:
        break
cap.release()
cv2.destroyAllWindows()


