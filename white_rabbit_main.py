#!/usr/bin/env python3

import threading
import rpyc
import numpy as np
from imutils.video import WebcamVideoStream
import cv2, time

conn = rpyc.classic.connect('192.168.32.209')
ev3 = conn.modules['ev3dev.ev3']

btn = ev3.Button()

mA = ev3.LargeMotor('outA')
mD = ev3.LargeMotor('outB')

P = 0.2
speed = 0
max = 0
x = 0
dArea = 0
size = 0

cap = WebcamVideoStream(src=0).start()
for i in range(10): frame = cap.read()

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
H = hsv[320,240, 0]
S = hsv[320,240, 1]
V = hsv[320,240, 2]
Lo = np.array([H-35, S-50, V-75])
Hi = np.array([H+35, S+50, V+75])

frame_gray = cv2.inRange(hsv, Lo, Hi)
cv2.imwrite('/var/www/html/kube_search.png', frame_gray)

def motor_control():
    global dArea, x, P, size, frame_gray
    while True:
        if(np.sum(frame_gray) > 10000):
            speedA = size*3 - (x*P)
            speedD = size*3 + (x*P)

            if(speedA > 900): speedA = 900
            if(speedA < -900): speedA = -900
            if(speedD > 900): speedD = 900
            if(speedD < -900): speedD = -900

            mA.run_forever(speed_sp=speedA)
            mD.run_forever(speed_sp=speedD)
        else:
            mA.stop(stop_action="brake")
            mD.stop(stop_action="brake")

t1 = threading.Thread(target=motor_control)
t1.daemon = True
t1.start()

while True:
    frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame_gray = cv2.inRange(hsv, Lo, Hi)
    if(np.sum(frame_gray) > 10000):

        moments = cv2.moments(frame_gray, 1)
        dM01 = moments['m01']
        dM10 = moments['m10']
        dArea = moments['m00']

        if(max==0): max = dArea
        size = 45 - (dArea / max * 100)

        if(dArea != 0):
            x = 320 - int(dM10 / dArea)
            y = 240 - int(dM01 / dArea)

        if(x>-10 and x < 10): x = 0
        if(size>-5 and size < 5): size = 0

    if(btn.backspace):
        size = 0
        x = 0
        break

mA.stop(stop_action="brake")
mD.stop(stop_action="brake")
