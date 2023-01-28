import cv2
from cv2 import aruco
import numpy as np

class Camera:
    def __init__(self):
        self.data = np.load("MultiMatrix.npz")

        self.camMatrix = self.data["camMatrix"]
        self.distCof = self.data["distCoef"]
        self.rVector = self.data["rVector"]
        self.tVector = self.data["tVector"]

        self.Marker_size    =   2.7 #centimeters
        self.Marker_dict    =   aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
        self.Para_markers   =   aruco.DetectorParameters()

        self.capture = cv2.VideoCapture(0, cv2.CAP_V4L2)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 10000)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 10000)
        self.capture.set(cv2.CAP_PROP_FPS, 60)
        self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

        (self.Xo,self.Yo) = (0,0)
        (self.x,self.y) = (0,0)
        self.coords_available = False
        self.pid = False


    def get_marker_data(self, dist, coords, assign):

        #  print("DEBUG::Inside Function")

        while True:
                #  print("DEBUG::Inside loop")
                ret,frame = self.capture.read()

                if ret==False:
                        print("INFO::Unable to read frame. Exiting")
                        break
                grayimg=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                marker_corners, marker_ids, reject = aruco.detectMarkers(grayimg,self.Marker_dict, parameters=self.Para_markers)

                if marker_corners:
                        (x1,y1)=(int(marker_corners[0][0][-1][0]),int(marker_corners[0][0][-1][1]))
                        (x2,y2)=(int(marker_corners[0][0][1][0]),int(marker_corners[0][0][1][1]))

                        (self.x,self.y)=((x1+x2)//2,(y1+y2)//2)

                        rVec, tVec, _ = aruco.estimatePoseSingleMarkers(marker_corners, self.Marker_size, self.camMatrix, self.distCof)
                        total_markers = range(0, marker_ids.size)
                        for j in range(len(marker_ids)):
                                for i in range(4):
                                        cv2.line(frame,(int(marker_corners[j][0][i-1][0]),int(marker_corners[j][0][i-1][1])),(int(marker_corners[j][0][i][0]),int(marker_corners[j][0][i][1])),(0,255,0),4)

                                point = cv2.drawFrameAxes(frame, self.camMatrix, self.distCof, rVec[j], tVec[j], 4, 4)
                                distance = np.sqrt(tVec[j][0][2] ** 2 + tVec[j][0][0] ** 2 + tVec[j][0][1] ** 2)
                                distance=185-distance
                                distance=(distance+22)/1.09
                                dist[0] = distance
                                assign(dist, coords)


                                cv2.putText(frame, f"{distance}", (70,80),  cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255),2,cv2.LINE_AA)

                                cv2.putText(frame,f"x:{round(rVec[j][0][0],1)} y: {round(rVec[j][0][1],1)} ",(70,150),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),2,cv2.LINE_AA)

                                X=self.x-self.Xo
                                Y=self.Yo-self.y
                                print(f"Inside ArUco: X : {X}")
                                print(f"Inside ArUco: Y : {Y}")
                                coords[0] = X
                                coords[1] = Y
                                assign(dist, coords)
                                self.coords_available = True

                                cv2.putText(frame,f"({X},{Y}),", (70,500),cv2.FONT_HERSHEY_PLAIN,3,(0, 0, 255),2,cv2.LINE_AA)

                cv2.imshow("frame",frame)

                key=cv2.waitKey(1)
                if key==ord("o"):
                    (self.Xo,self.Yo)=(self.x,self.y)
                if key==ord("x"):
                    cv2.imwrite("frame.png",frame)
                # capital P will stop pid, small p will begin
                if key==ord("p"):
                    self.pid == True
                if key==ord("P"):
                    self.pid = False
                elif key==ord("c"):
                        break

        self.capture.release()
        cv2.destroyAllWindows()

        exit()

d = [0]
coords = [0,0]
def assign(p_d, p_coords):
    global d
    global coords
    d = p_d
    coords = p_coords

if __name__ == "__main__":
    cam = Camera()
    print("Started..")
    while True:
        print("Getting Marker data")
        cam.get_marker_data(d, coords, assign)
