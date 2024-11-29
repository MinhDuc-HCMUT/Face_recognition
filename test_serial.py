import serial
import time


def main():
    # Cấu hình cổng COM và baud rate
    com_port = "COM12"
    baud_rate = 115200

    try:
        # Mở kết nối serial
        with serial.Serial(com_port, baud_rate, timeout=1) as ser:
            print(f"Đã kết nối tới {com_port} với baud rate {baud_rate}")

            # Gửi dữ liệu "True"
            data_to_send = "True"
            ser.write(data_to_send.encode('utf-8'))
            print(f"Đã gửi: {data_to_send}")

            # Đợi nhận dữ liệu phản hồi
            time.sleep(1)  # Chờ 1 giây để thiết bị gửi phản hồi
            if ser.in_waiting > 0:  # Kiểm tra nếu có dữ liệu trong buffer
                received_data = ser.read(ser.in_waiting).decode('utf-8').strip()
                print(f"Dữ liệu nhận được: {received_data}")
            else:
                print("Không nhận được dữ liệu từ thiết bị.")

    except serial.SerialException as e:
        print(f"Lỗi kết nối serial: {e}")
    except Exception as e:
        print(f"Lỗi không xác định: {e}")


if __name__ == "__main__":
    main()
