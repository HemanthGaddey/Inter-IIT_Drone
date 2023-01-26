import pyMultiWii
import time
import sys, select, termios, tty
import socket
ct = time.time()
def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
        if (key == '\x1b'):
            key = sys.stdin.read(2)
        sys.stdin.flush()
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key
HOST = '127.0.0.1'        
PORT = 60000
'''Control Your Drone!
---------------------------
Moving around:
   u    i    o
   j    k    l
   n    m    ,


spacebar : arm or disarm
w : increase height
s : decrease height
a : yaw left
d : yaw right
Up arrow : go forward
Down arrow : go backward
Left arrow : go left
Right arrow : go right

CTRL+C to quit

Function Name: getKey
Input: None
Output: keyboard charecter pressed
Logic: Determine the keyboard key pressed
Example call: getkey()
'''

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    settings = termios.tcgetattr(sys.stdin)
    msg_pub=0 # by default valuse should be 0
    keyboard_control={
                      '[A': 10,
                      '[D': 30,
                      '[C': 40,
                      'w':50,
                      's':60,
                      ' ': 70,
                      'r':80,
                      't':90,
                      'p':100,
                      '[B':110,
                      'n':120,
                      'a':150,
                      'd':160,
                      'g':170,
                      'q': 130,
                      'e': 140,
                      '+' : 15,
                      '1' : 25,
                      '2' : 30,
                      '3' : 35,
                      '4' : 45}

    control_to_change_value=('u','o',',','z','c')
    msg_list = []
    start=0
    threshold=0.01
    last = 80
    try:
        while True:
            # whilw time < 10ms:
            key = getKey()
            if (key == '\x03'):
                break

            if key in keyboard_control.keys():
                s.send(bytes(str(keyboard_control[key]), 'utf-8'))

            else :
            	if(time.time() - ct >= 22/1000):
		            s.send(bytes(str(42), 'utf-8'))
		            #s.send(bytes(str(80), 'utf-8'))
		            ct = time.time()

    finally:
        pass
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)


myDrone.disconnect()

