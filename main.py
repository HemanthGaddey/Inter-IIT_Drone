import ArUco
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from simple_pid.PID import PID
import pyMultiWii
import time
import sys, select, termios, tty
import socket

#------------ Drone --------------
#  myDrone = pyMultiWii.pyMultiWii("192.168.4.1", 23)

#-------------- PID --------------
Kp = 0.5
Ki = 0
Kd = 0
set_point = 0
pid_Roll = PID(Kp,Ki,Kd,set_point)
pid_Pitch = PID(Kp,Ki,Kd,set_point)
x_error = 0     #pixels
y_error = 0     #pixels
z_error = 0     #cm
pitch_pid_op = (False,1500)
roll_pid_op = (False,2500)
'''
# NOTE!!
# 1000-2000 : Throttle
# 1350-1650 : Pitch
# 2350-2650 : Roll
# 3350-3650 : Yaw
'''

def pid_function(cam):
    global coords
    while True:
        if(cam.coords_available):
            print("Coords received from camera")
            x_error = coords[0]/20.48 #system Res   #[-100,+100]
            y_error = coords[1]/15.36
            print(coords)
            if(x_error>=0):
                roll_pid_op = (True, 2600)
                print(f"Roll 1100")
            else:
                roll_pid_op = (True, 2400)
                print(f"Roll 900")

            if(y_error>=0):
                pitch_pid_op = (True, 3600)
                print(f"Pitch 1100")
            else:
                pitch_pid_op = (True, 3400)
                print(f"Pitch 900")

            #pitch_pid_op[1] = pid(y_error)*15 + 1500 + 1000
            #roll_pid_op[1] = pid(x_error)*15 + 1500 + 2000

            cam.coords_available = False


#-------------- Aruco OpenCV Object --------------
cam = ArUco.Camera()
d = [0]
coords = [0,0]
def assign(p_d, p_coords):
    global d
    global coords
    d = p_d
    coords = p_coords

#-------------- MATPLOTLIB --------------
x_len = 200         # Number of points to display
y_range = [0, 184]  # Range of possible Y values to display

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = list(range(0, 200))
ys = [0] * x_len
ax.set_ylim(y_range)
# Add labels
plt.title('PID ;)')
plt.xlabel('Time')
plt.ylabel('Height(cm)')

# Create a blank line. We will update the line in animate
line, = ax.plot(xs, ys)

def animate(i, ys):
    global d

    temp_c = d[0]

    ys.append(temp_c) # Add y to list
    ys = ys[-x_len:] # Limit y list to set number of items

    line.set_ydata(ys) # Update line with new Y values

    return line,

#  ani = animation.FuncAnimation(fig,
#      animate,
#      fargs=(ys,),
#      interval=5,
#      blit=True)

#-------------- a.PY --------------
HOST = '127.0.0.1'
PORT = 60000
settings = termios.tcgetattr(sys.stdin)

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

def a_py():
        ct = time.time()
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
                        if pitch_pid_op[0]:
                            s.send(bytes(str(pitch_pid_op[1]),'utf-8'))
                            pitch_pid_op[0] = False
                        if roll_pid_op[0]:
                            s.send(bytes(str(roll_pid_op[1]),'utf-8'))
                            roll_pid_op[0] = False
                        elif(time.time()-ct >= 22/1000):
                            s.send(bytes(str(80), 'utf-8'))
                            ct = time.time()
                        else:
                            s.send(bytes(str(10),'utf-8'))
                            s.send(bytes(str(40),'utf-8'))


                finally:
                    pass
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)


        myDrone.disconnect()

#-------------- Main --------------
def print_data():
    while True:
        print(d[0],pitch_pid_op[1]-1000,roll_pid_op[1]-2000)

if __name__ == '__main__':
    print(1)
    cam_thread = threading.Thread(target=cam.get_marker_data, args=(d, coords, assign))
    #  data_print_thread = threading.Thread(target=print_data, args=())
    #  a_py_thread = threading.Thread(target=a_py, args=())
    pid_thread = threading.Thread(target=pid_function, args=(cam, ))

    cam_thread.start()
    pid_thread.start()
    #data_print_thread.start()
    #  a_py_thread.start()

    #  plt.show()
    #  state = 0
    #  init_time = time.time()
    #  ct = time.time()
    #  ct = time.time()
    #  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #      s.connect((HOST, PORT))
    pid_thread.join()
    cam_thread.join()
    while False:
        if state == 0:
            print("DEBUG::Arming")
            myDrone.arm()
            #  s.send(bytes("70", 'utf-8'))
            state = 5
        elif state == 5:
            if(time.time() - init_time > 0.5):
                print("DEBUG::Taking off")
                #  s.send(bytes("130",'utf-8'))
                myDrone.take_off()
                state = 10
        elif state == 10:
            if(time.time() - init_time > 1):
                print("DEBUG::Moving")
                #  s.send(bytes(str(2600),'utf-8'))
                myDrone.setPitch(1100)
                state = 20
        elif state == 20:
            if(time.time() - init_time > 2):
                print("DEBUG::Moving")
                #  s.send(bytes(str(3600),'utf-8'))
                myDrone.setRoll(1100)
                state = 30
        elif state == 30:
            if(time.time() - init_time > 3):
                print("DEBUG::Landing")
                #  s.send(bytes(str(140),'utf-8'))
                myDrone.land()
                state = 40
        elif state == 40:
            if(time.time() - init_time > 4):
                print("DEBUG::Disarming")
                #  s.send(bytes(str(170),'utf-8'))
                myDrone.disarm()
                state = 50
        if(time.time() - ct >= 22/1000):
            #  s.send(bytes(str(80), 'utf-8'))
            myDrone.reset()
            ct = time.time()

