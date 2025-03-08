import socket
import sys
import time
BT_HOST = "E4:5F:01:F6:75:36" # The address of Raspberry PI Bluetooth adapter on the server.
BT_PORT = 10

print("Starting Bluetooth Client")

try:
    with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as s:
        s.connect((BT_HOST, BT_PORT))

        try:
            while True:
            
                data = s.recv(1024).decode().strip()
            
                if data:
                    print(data)
                    s.sendall(f"Ack (BT): {data}".encode())
                    sys.stdout.flush()
                    time.sleep(0.1)

        except KeyboardInterrupt:
            print("Closing Bluetooth Connection")
            s.close()
except Exception as e:
    print("Error: ", e)