#!/usr/bin/env python3       

import pyMultiWii
import socket
import time
myDrone=pyMultiWii.pyMultiWii("192.168.4.1", 23)
last_cmd = None
def indentify_key(msg):
                key_value = int(msg)
                print(key_value)
                if key_value == 70:
                    myDrone.arm()
                elif key_value == 170:
                    myDrone.disarm()
                elif key_value == 10: # forward
                    myDrone.setPitch(1600)
                elif key_value == 30: #left
                    myDrone.setRoll(1400)
                elif key_value == 40: #right
                    myDrone.setRoll(1600)
                elif key_value == 80 and myDrone.armed: #reset 
                    myDrone.reset()
                elif key_value == 42:
                    myDrone.spl_throttle_mode_reset(myDrone.throttle)
                elif key_value == 50: #increase height
                    if(myDrone.throttle <= 1950):   #myDrone.setThrottle(1800)
                        myDrone.throttle += 50
                elif key_value == 60: #decrease height
                    if(myDrone.throttle > 50): #myDrone.setThrottle(1300)
                        myDrone.throttle -= 50
                elif key_value == 110: #backward
                    myDrone.setPitch(1400)
                #elif key_value == 130:
                  #      take_off()
                #elif key_value == 140:
                 #       land()
                elif key_value == 150: #left_yaw
                    myDrone.setYaw(1200)
                elif key_value == 160: #right yaw
                    myDrone.setYaw(1800)
                elif key_value == 130:
                    myDrone.take_off()
                elif key_value == 140:
                    myDrone.land()
                elif key_value == 90:
                    # myDrone.throttleMode(1)
                    myDrone.Array[17] = 220
                    myDrone.Array[18] = 5
                elif key_value == 120:
                    myDrone.Array[17] = 232
                    myDrone.Array[18] = 3
                    # print('here')
                    # myDrone.setThrottle(0)
                    # myDrone.reset()



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
                
                time.sleep(22/1000)
                print(myDrone.throttle)
                
                indentify_key(data)
