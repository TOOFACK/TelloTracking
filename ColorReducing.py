import cv2
import numpy as np

c = cv2.VideoCapture(0)


def em():
    pass


cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 240)
cv2.createTrackbar("HUE Min", "HSV", 0, 179, em)
cv2.createTrackbar("HUE Max", "HSV", 179, 179, em)
cv2.createTrackbar("SAT Min", "HSV", 0, 255, em)
cv2.createTrackbar("SAT Max", "HSV", 255, 255, em)
cv2.createTrackbar("VALUE Min", "HSV", 0, 255, em)
cv2.createTrackbar("VALUE Max", "HSV", 255, 255, em)

while True:
    _, img = c.read()
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    mask = cv2.inRange(imgHsv, lower, upper)
    result = cv2.bitwise_and(img, img, mask = mask)


    cv2.imshow("Orig", np.vstack((result, img)))
    cv2.imshow("a", mask)

    # cv2.imshow("a", imgHsv)
    # cv2.imshow("ch", result)

    if cv2.waitKey(5) == 27:
        break
cv2.destroyAllWindows()
