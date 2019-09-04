import cv2
import sys
import os
import time
from enum import Enum
from djitellopy import Tello

class State (Enum):

    detectingFaces = 1
    goingToPerson = 2

state = State.detectingFaces

S=60
FPS=30

distanceThreshold= 200

speed= 10

currentScreenshot = 1


TOLERANCE_X = 4
TOLERANCE_Y = 4
SLOWDOWN_THRESHOLD_X = 20
SLOWDOWN_THRESHOLD_Y = 2
DRONE_SPEED_X = 10
DRONE_SPEED_Y = 10
SET_POINT_X = 480
SET_POINT_Y = 360


faceCascade = cv2.CascadeClassifier("faced.xml")
drone = Tello() #  tello o drone = Tello() declaramos tello como objeto.
drone.connect()
drone.takeoff()
drone.move_up(200)
time.sleep(2)
drone.streamon()  # start camera streaming


# video_capture = cv2.VideoCapture("udp://0.0.0.0:11111")
# video_capture = cv2.VideoCapture("rtsp://192.168.1.1")
# video_capture = cv2.VideoCapture(0)

while True:
    
    # ret, frame = video_capture.read()
    

    frame = drone.get_frame_read().frame  # capturing frame from drone
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # turning image into gray scale

    faces = faceCascade.detectMultiScale(  # face detection
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    if state == State.detectingFaces:
        drone.rotate_clockwise(15)
        time.sleep(1)
    i = 0
    # Decorating image for debug purposes and looping through every detected face
    for (x, y, w, h) in faces:

        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 5)  # contour rectangle
        cv2.circle(frame, (int(x+w/2), int(y+h/2)), 12, (255, 0, 0), 1)  # face-centered circle
        # print(frame.shape)
        # cv2.line(frame, (int(x+w/2), int(720/2)), (int(960/2), int(720/2)), (0, 255, 255))

        cv2.circle(frame, (int(SET_POINT_X), int(SET_POINT_Y)), 12, (255, 255, 0), 8)  # setpoint circle
        i = i+1
        distanceX = x+w/2 - SET_POINT_X
        distanceY = y+h/2 - SET_POINT_Y

        up_down_velocity = 0
        right_left_velocity = 0
        if state == State.detectingFaces:
            state = State.goingToPerson

        if distanceX < -TOLERANCE_X:
            print("Mover dron a la izquierda")
            right_left_velocity = - DRONE_SPEED_X

        elif distanceX > TOLERANCE_X:
            print("Mover el dron a la derecha")
            right_left_velocity = DRONE_SPEED_X
        else:
            print("OK")

        if distanceY < -TOLERANCE_Y:
            print("Mover el dron para arriba")
            up_down_velocity = DRONE_SPEED_Y
        elif distanceY > TOLERANCE_Y:
            print("Mover el dron para abajo")
            up_down_velocity = - DRONE_SPEED_Y

        else:
            print("OK")

        if abs(distanceX) < SLOWDOWN_THRESHOLD_X:
            right_left_velocity = int(right_left_velocity / 2)
        if abs(distanceY) < SLOWDOWN_THRESHOLD_Y:
            up_down_velocity = int(up_down_velocity / 2)

        drone.send_rc_control(right_left_velocity, 0, up_down_velocity, 0)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # quit from script
        break

# video_capture.release()
drone.land()
drone.streamoff()
cv2.destroyAllWindows()
sys.exit()

