import cv2
import numpy as np
import sqlite3
import os
import serial
import time  # Thư viện để quản lý thời gian
from PIL import Image

def insertOrUpdate(id, name):
    conn = sqlite3.connect("D:/DATN/test_serial/test_serial/data.db")
    query = "SELECT * FROM people WHERE ID=" + str(id)
    cursor = conn.execute(query)
    isRecordExist = 0

    for row in cursor:
        isRecordExist = 1
    if isRecordExist == 0:
        query = "INSERT INTO people(ID,Name) VALUES(" + str(id) + ",'" + str(name) + "')"
    else:
        query = "UPDATE people SET Name='" + str(name) + "' WHERE ID=" + str(id)
    conn.execute(query)
    conn.commit()
    conn.close()

def checkInDatabase(id, name):
    conn = sqlite3.connect("D:/DATN/test_serial/test_serial/data.db")
    query = "SELECT * FROM people WHERE ID=? AND Name=?"
    cursor = conn.execute(query, (id, name))
    result = cursor.fetchone()  # Lấy một kết quả
    conn.close()
    return result is not None  # Trả về True nếu có dữ liệu, False nếu không

def deleteData(id, name):
    try:
        # Xóa ảnh của user trong thư mục dataSet
        user_images_path = 'dataSet'  # Thư mục chứa tất cả ảnh của người dùng
        # Duyệt qua tất cả các tệp trong thư mục 'dataSet'
        deleted = False
        for filename in os.listdir(user_images_path):
            if filename.startswith(f"User.{id}."):
                file_path = os.path.join(user_images_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)  # Xóa tệp ảnh
                    deleted = True  # Đánh dấu nếu có tệp bị xóa
        if deleted:
            print(f"Đã xóa tất cả ảnh của User.{id}")
        else:
            print(f"Không tìm thấy ảnh của User.{id} để xóa.")

        # Xóa bản ghi trong database
        conn = sqlite3.connect("D:/DATN/test_serial/test_serial/data.db")
        query = "DELETE FROM people WHERE ID=? AND Name=?"
        conn.execute(query, (id, name))
        conn.commit()
        conn.close()

        print(f"Đã xóa dữ liệu của User.{id} trong cơ sở dữ liệu.")
        return True  # Trả về True nếu xóa thành công
    except Exception as e:
        print(f"Lỗi khi xóa dữ liệu: {e}")
        return False  # Trả về False nếu có lỗi


# Hàm xóa tất cả dữ liệu người dùng và ảnh, tạo tệp mô hình giả
def deleteAllData():
    try:
        # Xóa tất cả ảnh .jpg trong thư mục dataSet
        user_images_path = 'dataSet'  # Thư mục chứa tất cả ảnh của người dùng
        deleted = False
        for filename in os.listdir(user_images_path):
            if filename.endswith(".jpg"):  # Chỉ xóa các ảnh .jpg
                file_path = os.path.join(user_images_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)  # Xóa tệp ảnh
                    deleted = True  # Đánh dấu nếu có tệp bị xóa
        if deleted:
            print("Đã xóa tất cả ảnh trong thư mục dataSet.")
        else:
            print("Không tìm thấy ảnh để xóa.")

        # Xóa tất cả bản ghi trong bảng people
        conn = sqlite3.connect("D:/DATN/test_serial/test_serial/data.db")
        query = "DELETE FROM people"
        conn.execute(query)
        conn.commit()
        conn.close()

        print("Đã xóa tất cả dữ liệu trong cơ sở dữ liệu.")

        # Tạo tệp trainingData.yml giả
        createFakeTrainingData()

        return True  # Trả về True nếu xóa thành công
    except Exception as e:
        print(f"Lỗi khi xóa dữ liệu: {e}")
        return False  # Trả về False nếu có lỗi


# Hàm tạo tệp trainingData.yml giả (dữ liệu không hợp lệ)
def createFakeTrainingData():
    # Tạo dữ liệu giả (ID = -1, không có ảnh thực tế)
    faces = [np.zeros((100, 100), dtype=np.uint8)]  # Ảnh trắng kích thước 100x100
    IDs = [-1]  # ID giả

    # Huấn luyện mô hình với dữ liệu giả
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(IDs))

    # Lưu mô hình giả vào tệp trainingData.yml
    if not os.path.exists('recognizer'):
        os.makedirs('recognizer')

    recognizer.save('recognizer/trainingData.yml')
    print("Đã tạo tệp trainingData.yml giả!")


# Hàm lấy ảnh và ID từ thư mục dataSet
def getImageWithID(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    IDs = []
    for imagePath in imagePaths:
        faceImg = Image.open(imagePath).convert('L')
        faceNp = np.array(faceImg, 'uint8')
        print(faceNp)
        Id = int(imagePath.split('\\')[1].split('.')[1])
        faces.append(faceNp)
        IDs.append(Id)
        cv2.imshow('training', faceNp)
        cv2.waitKey(10)
    return faces, IDs


# Hàm huấn luyện lại mô hình nhận diện gương mặt
def trainRecognizer():
    # Đọc dữ liệu từ thư mục 'dataSet'
    faces, IDs = getImageWithID('dataSet')

    # Huấn luyện lại mô hình nhận diện
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(IDs))

    # Lưu lại mô hình nhận diện
    if not os.path.exists('recognizer'):
        os.makedirs('recognizer')

    recognizer.save('recognizer/trainingData.yml')
    print("Huấn luyện lại mô hình thành công và đã lưu!")

# Cấu hình serial
serial_port = "COM12"  # Thay bằng cổng serial của bạn
baud_rate = 115200
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# Thư viện nhận diện gương mặt
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Khởi động webcam với biến cap
cap = cv2.VideoCapture(0)

sampleNum = 0
id = None
name = None

# Biến theo dõi thời gian
start_time = time.time()

# Biến flag để kiểm soát capture ảnh
capture_faces = False

while True:
    # Kiểm tra dữ liệu từ serial
    if ser.in_waiting > 0:
        serial_data = ser.readline().decode('utf-8').strip()
        print(f"Dữ liệu từ serial: {serial_data}")

        if serial_data.startswith("Add."):
            try:
                # Làm sạch dữ liệu và lấy ID
                clean_data = serial_data.replace("\x00", "").strip()
                id = int(clean_data.split(".")[1])
                name = f"USER{id}"  # Gán tên mặc định là USER + ID
                print(f"Thêm/ cập nhật ID: {id}, Tên: {name}")
                insertOrUpdate(id, name)

                # Bật chế độ capture khi nhận Add.X
                capture_faces = True

                # Reset thời gian vì nhận được dữ liệu
                start_time = time.time()

            except (ValueError, IndexError) as e:
                print(f"Lỗi khi xử lý dữ liệu serial: {e}")

        elif serial_data.startswith("Che."):
            try:
                # Làm sạch dữ liệu và lấy ID
                clean_data = serial_data.replace("\x00", "").strip()
                id = int(clean_data.split(".")[1])
                name = f"USER{id}"  # Gán tên mặc định là USER + ID
                print(f"Kiểm tra ID: {id}, Tên: {name}")

                # Kiểm tra trong cơ sở dữ liệu
                if checkInDatabase(id, name):
                    ser.write(b"TRUE")  # Gửi "TRUE" qua serial
                    print("Dữ liệu tồn tại trong DB, đã gửi: TRUE")
                else:
                    ser.write(b"FALSE")  # Gửi "FALSE" qua serial
                    print("Dữ liệu không tồn tại trong DB, đã gửi: FALSE")

                # Tắt chế độ capture khi nhận Che.X
                capture_faces = False

                # Reset thời gian vì nhận được dữ liệu
                start_time = time.time()

            except (ValueError, IndexError) as e:
                print(f"Lỗi khi xử lý dữ liệu serial: {e}")

        elif serial_data.startswith("Rem."):
            try:
                # Làm sạch dữ liệu và lấy ID
                clean_data = serial_data.replace("\x00", "").strip()
                id = int(clean_data.split(".")[1])
                name = f"USER{id}"  # Gán tên mặc định là USER + ID
                print(f"Yêu cầu xóa ID: {id}, Tên: {name}")

                # Xóa dữ liệu ảnh và bản ghi trong database
                success = deleteData(id, name)

                # Gửi thông báo "True" hoặc "False" qua serial khi xóa thành công hoặc thất bại
                if success:
                    ser.write(b"True")
                    print("Đã gửi: True")
                else:
                    ser.write(b"False")
                    print("Đã gửi: False")

                #Huấn luyện lại mô hình khi xóa dữ liệu
                if os.listdir('dataSet'):  # Kiểm tra thư mục còn dữ liệu hay không
                    trainRecognizer()
                else:
                    createFakeTrainingData()  # Tạo tệp mô hình giả nếu không còn dữ liệu

            except (ValueError, IndexError) as e:
                print(f"Lỗi khi xử lý dữ liệu serial: {e}")

        elif serial_data == "Del.ALL":
            print("Yêu cầu xóa tất cả dữ liệu...")
            # Xóa tất cả ảnh và dữ liệu trong database
            success = deleteAllData()

            # Gửi thông báo "True" hoặc "False" qua serial khi xóa thành công hoặc thất bại
            if success:
                ser.write(b"True")
                print("Đã gửi: True")
            else:
                ser.write(b"False")
                print("Đã gửi: False")

    # Nếu không nhận được dữ liệu trong 30 giây
    if time.time() - start_time > 30:
        ser.write(b"FALSE")  # Gửi "FALSE" qua serial khi hết thời gian chờ
        print("Không nhận được dữ liệu trong 30 giây, đã gửi: FALSE")
        break

    # Chỉ capture nếu ID không phải None và capture_faces là True
    if id is not None and capture_faces:
        # Đọc dữ liệu từ webcam
        ret, frame = cap.read()
        if not ret:
            print("Không thể truy cập webcam")
            break

        # Chuyển dữ liệu ảnh đầu vào thành ảnh xám
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Gọi hàm nhận diện gương mặt
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Vẽ hình chữ nhật quanh các khuôn mặt phát hiện được
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            if not os.path.exists('dataSet'):
                os.makedirs('dataSet')

            sampleNum += 1
            cv2.imwrite('dataSet/User.' + str(id) + "." + str(sampleNum) + ".jpg", gray[y: y + h, x: x + w])

        cv2.imshow('frame', frame)
        cv2.waitKey(1)

        if sampleNum > 499:
            # Gửi xác nhận "True" qua serial
            # Huấn luyện lại mô hình khi thêm dữ liệu
            trainRecognizer()
            ser.write(b"True")
            print("Đã gửi: True")
            break

cap.release()
cv2.destroyAllWindows()
ser.close()
