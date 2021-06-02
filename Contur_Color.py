import cv2
import numpy as np

c = cv2.VideoCapture(0)


def em():
    pass


cv2.namedWindow("Params")
cv2.createTrackbar("T_Hold1", "Params", 23, 255, em)
cv2.createTrackbar("T_Hold2", "Params", 25, 255, em)
cv2.createTrackbar("Area", "Params", 5000, 30000, em)

cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 240)
cv2.createTrackbar("HUE Min", "HSV", 0, 179, em)
cv2.createTrackbar("HUE Max", "HSV", 179, 179, em)
cv2.createTrackbar("SAT Min", "HSV", 0, 255, em)
cv2.createTrackbar("SAT Max", "HSV", 255, 255, em)
cv2.createTrackbar("VALUE Min", "HSV", 0, 255, em)
cv2.createTrackbar("VALUE Max", "HSV", 255, 255, em)


def getCountours(img, imgContour):
    conts, hierarch = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in conts:
        area = cv2.contourArea(cnt)
        areaMin = cv2.getTrackbarPos("Area", "Params")
        if area > areaMin:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            print(len(approx))
            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour, (x, y,), (x + w, y + h), (0, 255, 0), 5)


while (1):
    _, f = c.read()

    imgHsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    mask = cv2.inRange(imgHsv, lower, upper)
    result = cv2.bitwise_and(f, f, mask=mask)


    imgB = cv2.GaussianBlur(result, (7, 7), 1)
    imgGray = cv2.cvtColor(imgB, cv2.COLOR_BGR2GRAY)

    threshold1 = cv2.getTrackbarPos("T_Hold1", "Params")
    threshold2 = cv2.getTrackbarPos("T_Hold2", "Params")
    imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
    imgDil = cv2.dilate(imgCanny, np.ones((5, 5)), iterations=1)

    imgConts = f.copy()

    getCountours(imgDil, imgConts)

    cv2.imshow('track', imgConts)
    cv2.imshow("Orig", np.vstack((result, f)))
    if cv2.waitKey(5) == 27:
        break
cv2.destroyAllWindows()
