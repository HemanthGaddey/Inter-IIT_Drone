import ArUco
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from simple_pid import PID
import pyMultiWii
import time
import sys, select, termios, tty
import socket


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

    if(cam.coords_available):
        pitch_pid_op[0] = True
        roll_pid_op[0] = True

        x_error = coords[0]/20.48 #system Res	#[-100,+100]
        y_error = coords[1]/15.36
        if(x_error>=0):
        	roll_pid_op[1] = 2600
        else:
        	roll_pid_op[1] = 2400
        
        if(y_error>=0):
        	pitch_pid_op[1] = 3600
        else:
        	pitch_pid_op[1] = 3400
			
        #pitch_pid_op[1] = pid(y_error)*15 + 1500 + 1000
        #roll_pid_op[1] = pid(x_error)*15 + 1500 + 2000
        
        cam.coords_available = False


#-------------- Aruco OpenCV Object --------------
cam = ArUco.Camera()
d = [0]
coords = [0,0]
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

ani = animation.FuncAnimation(fig,
    animate,
    fargs=(ys,),
    interval=5,
    blit=True)
    
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
                        #if pitch_pid_op[0]:
                        	#s.send(bytes(str(pitch_pid_op[1]),'utf-8'))
                        	#pitch_pid_op[0] = False
                        #if roll_pid_op[0]:
                            #s.send(bytes(str(roll_pid_op[1]),'utf-8'))
                            #roll_pid_op[0] = False
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

    cam_thread = threading.Thread(target=cam.get_marker_data, args=(d,coords,))
    #data_print_thread = threading.Thread(target=print_data, args=())
    a_py_thread = threading.Thread(target=a_py, args=())
        
    cam_thread.start()
    #data_print_thread.start()
    a_py_thread.start()
    
    plt.show()
    
