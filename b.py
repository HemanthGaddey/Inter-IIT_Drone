#!/usr/bin/env python3       

import pyMultiWii
import socket
import time
myDrone=pyMultiWii.pyMultiWii("192.168.4.1", 23)
last_cmd = None
mode = 'alt_hold' #or throttle
def indentify_key(msg):
                key_value = int(msg)
                print(key_value)
                if key_value == 70:
                    myDrone.arm()
                elif key_value == 170:
                    myDrone.disarm()
                elif key_value == 10: # forward
                    myDrone.setPitch(1700) #changed from 1600 to 1700
                elif key_value == 30: #left
                    myDrone.setRoll(1400)
                elif key_value == 40: #right
                    myDrone.setRoll(1700) #changed from 1600 to 1700
                elif key_value == 80 and myDrone.armed: #reset 
                    myDrone.reset()
                elif key_value == 50: #increase height
                    myDrone.setThrottle(1800)
                elif key_value == 60: #decrease height
                    myDrone.setThrottle(1300)
                elif key_value == 110: #backward
                    myDrone.setPitch(1400)
                elif key_value == 150: #left_yaw
                    myDrone.setYaw(1200)
                elif key_value == 160: #right yaw
                    myDrone.setYaw(1800)
                elif key_value == 130:
                    myDrone.take_off()
                elif key_value == 140:
                    myDrone.land()
                elif key_value == 90:
                	mode = "alt_hold"
                	myDrone.Array[17] = 220
                	myDrone.Array[18] = 5
                elif key_value == 120:
	                mode = "throttle"
	                myDrone.Array[17] = 232
	                myDrone.Array[18] = 3
                elif (key_value >= 1000 and key_value <= 2000):	#Variable Throttle
                	print(f"Setting Throttle {key_value}")
                	myDrone.setThrottle(key_value)
                elif (key_value >= 2350 and key_value <= 2650):	#Variable Pitch
                	print(f"Setting pitch {key_value}")
                	myDrone.setPitch(key_value-1500)
                elif (key_value >= 3350 and key_value <= 3650):	#Variable Roll
                	print(f"Setting Roll {key_value}")
                	myDrone.setRoll(key_value-2500)
                elif (key_value >= 4350 and key_value <= 4650):	#Variable Yaw
                	print(f"Setting Yaw {key_value}")
                	myDrone.setYaw(key_value-3500)



HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 60000        # Port to listen on (non-privileged ports are > 1023)
print("Server started : ")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn: 
        while True:
            #Name
            # try:
                data = conn.recv(1024).decode()
                indentify_key(data)
