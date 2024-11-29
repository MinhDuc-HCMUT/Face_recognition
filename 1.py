import cv2
import numpy as np

# Thư viện nhận diện gương mặt
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Khởi động webcam với biến cap
cap = cv2.VideoCapture(0)

while True:  # Ngắt vòng lặp khi nhấn Q hoặc X
    # Đọc dữ liệu từ webcam
    ret, frame = cap.read()
    if not ret:
        print("Không thể truy cập webcam")
        break

    # Chuyển dữ liệu ảnh đầu vào thành ảnh xám
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Gọi hàm nhận diện gương mặt
    faces = face_cascade.detectMultiScale(gray)

    # Vẽ hình chữ nhật quanh các khuôn mặt phát hiện được
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Hiển thị hình ảnh
    cv2.imshow('DETECT FACE', frame)

    # Thoát chương trình khi nhấn phím 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng webcam và đóng các cửa sổ
cap.release()
cv2.destroyAllWindows()
