import socket
from picar import front_wheels, back_wheels
from picar.SunFounder_PCA9685 import Servo
import picar
import car_stats
import json
import threading
from dataclasses import asdict
from gpiozero import CPUTemperature

cpu = CPUTemperature()

bw = back_wheels.Back_Wheels()
bw.speed = 0

fw = front_wheels.Front_Wheels()
fw.offset = 0

picar.setup()

stats = car_stats.CarStats("Straight", bw._speed, cpu.temperature)

WIFI_PORT = 65432           # Port to listen on
WIFI_HOST = "192.168.1.47"  # IP address of your Raspberry Pi

BT_PORT = 10              # Port to listen on
BT_HOST = "E4:5F:01:F6:75:36"  # IP address of your Raspberry Pi

def control_car(command):
    if command == "FORWARD":
        print("Moving forward")
        bw.speed = 50
        bw.backward()
    elif command == "BACKWARD":
        print("Moving backward")
        bw.speed = 50
        bw.forward()
    elif command == "LEFT":
        print("Turning left")
        fw.turn_left()
        stats.turning = "Left"
    elif command == "RIGHT":
        print("Turning right")
        fw.turn_right()
        stats.turning = "Right"
    elif command == "STOP":
        print("Stopping")
        fw.turn_straight()
        bw.speed = 0
        stats.turning = "Straight"
        bw.stop()
    else:
        print("Unknown command:", command)

def wifi():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((WIFI_HOST, WIFI_PORT))
        s.listen()

        try:
            while True:
                client, clientInfo = s.accept()
                print("Server received connection from:", clientInfo)

                data = client.recv(1024).decode().strip()  # Receive data and decode
                if data:
                    print("Received Command: ", data)
                    control_car(data)
                    client.sendall(f"Ack (WiFi): {data}".encode())

        except KeyboardInterrupt:
            print("Closing Wi-Fi server")
            fw.turn_straight()
            stats.turning = "Straight"
            bw.speed = 0
            bw.stop()
            s.close()

def bluetooth():
    with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as s:
        s.bind((BT_HOST, BT_PORT))
        s.listen()

        try:
            while True:
                client, clientInfo = s.accept()
                print("Server received connection from:", clientInfo)


                while True:
                    
                    stats.carSpeed = bw._speed
                    stats.cpuTemp = cpu.temperature
                    
                    payload = json.dumps(asdict(stats))
                    client.sendall(payload.encode())
                
                    data = client.recv(1024).decode().strip()  # Receive data and decode
                    if data:
                        print("Client Response:", data)

        except KeyboardInterrupt:
            print("Closing Bluetooth server")
            s.close()
            
wifi_thread = threading.Thread(target=wifi)
bluetooth_thread = threading.Thread(target=bluetooth)

wifi_thread.start()
bluetooth_thread.start()

wifi_thread.join()
bluetooth_thread.join()