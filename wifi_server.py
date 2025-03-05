import socket
from picar import front_wheels, back_wheels
from picar.SunFounder_PCA9685 import Servo
import picar

bw = back_wheels.Back_Wheels()
bw.speed = 50

fw = front_wheels.Front_Wheels()
fw.offset = 0

picar.setup()

PORT = 65432           # Port to listen on
HOST = "192.168.1.35"  # IP address of your Raspberry Pi

def control_car(command):
    if command == "FORWARD":
        print("Moving forward")
        bw.backward()
    elif command == "BACKWARD":
        print("Moving backward")
        bw.forward()
    elif command == "LEFT":
        print("Turning left")
        fw.turn_left()
    elif command == "RIGHT":
        print("Turning right")
        fw.turn_right()
    elif command == "STOP":
        print("Stopping")
        fw.turn_straight()
        bw.speed = 0
        bw.stop()
    else:
        print("Unknown command:", command)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    try:
        while True:
            client, clientInfo = s.accept()
            print("Server received connection from:", clientInfo)

            data = client.recv(1024).decode().strip()  # Receive data and decode
            if data:
                print("Received:", data)
                control_car(data)  # Handle car control
                client.sendall(f"Ack: {data}".encode())  # Send acknowledgment

    except KeyboardInterrupt:
        print("Closing server")
        fw.turn_straight()
        bw.speed = 0
        bw.stop()
        s.close()
