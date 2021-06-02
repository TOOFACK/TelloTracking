import cv2
import numpy as np

frameW  =640
frameH = 480
cap  =cv2.VideoCapture(1)
cap.set(3,frameW)
cap.set(4, frameH)


deadZone = 100
global imgCounter

def empty(a):
    pass

cv2.namedWindow("HSV")
cv2.resize("HSV", 640, 240)
cv2.createTrackbar("HUE min", "HSV", 19, 179, empty)

while True:
    _, img = cap.read()
    