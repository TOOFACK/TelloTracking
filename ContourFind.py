import cv2
import numpy as np

c = cv2.VideoCapture(0)


def em():
    pass


cv2.namedWindow("Params")
cv2.createTrackbar("T_Hold1", "Params", 23, 255, em)
cv2.createTrackbar("T_Hold2", "Params", 25, 255, em)
cv2.createTrackbar("Area", "Params", 5000, 30000, em)



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

    imgB = cv2.GaussianBlur(f, (7, 7), 1)
    imgGray = cv2.cvtColor(imgB, cv2.COLOR_BGR2GRAY)

    threshold1 = cv2.getTrackbarPos("T_Hold1", "Params")
    threshold2 = cv2.getTrackbarPos("T_Hold2", "Params")
    imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
    imgDil = cv2.dilate(imgCanny, np.ones((5, 5)), iterations=1)

    imgConts = f.copy()

    getCountours(imgDil, imgConts)

    cv2.imshow('e2', np.vstack((imgCanny,imgDil)))
    cv2.imshow("a", imgConts)
    if cv2.waitKey(5) == 27:
        break
cv2.destroyAllWindows()
