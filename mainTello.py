

import cv2
from djitellopy import Tello
import numpy as np

me = Tello()
me.connect()
me.RESPONSE_TIMEOUT = 2

def mainTello():


    startCount = 0

    width = 640
    height = 480
    deadZone = 100




    print(me.get_battery())
    me.for_back_velocity = 0
    me.left_right_velocity = 0
    me.up_down_velocity = 0
    me.yaw_velocity = 0
    me.speed = 0


    global dir


    me.streamoff()
    me.streamon()




    def em():
        pass


    cv2.namedWindow("Params")
    cv2.createTrackbar("T_Hold1", "Params", 23, 255, em)
    cv2.createTrackbar("T_Hold2", "Params", 25, 255, em)
    cv2.createTrackbar("Area", "Params", 5000, 30000, em)

    cv2.namedWindow("HSV")
    cv2.resizeWindow("HSV", 640, 240)
    cv2.createTrackbar("HUE Min", "HSV", 97, 179, em)
    cv2.createTrackbar("HUE Max", "HSV", 179, 179, em)
    cv2.createTrackbar("SAT Min", "HSV", 126, 255, em)
    cv2.createTrackbar("SAT Max", "HSV", 255, 255, em)
    cv2.createTrackbar("VALUE Min", "HSV", 85, 255, em)
    cv2.createTrackbar("VALUE Max", "HSV", 255, 255, em)


    def getCountours(img, imgContour):
        global dir
        conts, hierarch = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        for cnt in conts:
            area = cv2.contourArea(cnt)
            areaMin = cv2.getTrackbarPos("Area", "Params")
            if area > areaMin:
                cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                # print(len(approx))
                x, y, w, h = cv2.boundingRect(approx)
                cv2.rectangle(imgContour, (x, y,), (x + w, y + h), (0, 255, 0), 5)

                center_x = int(x + (w / 2))
                center_y = int(y + (h / 2))

                if center_x < int(width/2) - deadZone:
                    cv2.putText(imgContour, "GO LEFT", (20,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 3)
                    cv2.rectangle(imgContour, (0, int(height/2 - deadZone)),
                                  (int(width/2) - deadZone, int(height/2) + deadZone), (0, 255, 255), cv2.FILLED)
                    dir = 1

                elif center_y > int(height/2) + deadZone:
                    cv2.putText(imgContour, "GO DOWN", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 3)
                    cv2.rectangle(imgContour, (int(width / 2 - deadZone), int(height/2)+deadZone),
                                  (int(width / 2) + deadZone, height), (0, 255, 255), cv2.FILLED)
                    dir = 4

                elif center_y < int(height/2) - deadZone:
                    cv2.putText(imgContour, "GO UP", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 3)
                    cv2.rectangle(imgContour, (int(width / 2 + deadZone),int(height/2)-deadZone ),
                                  (width, int(height/2)-deadZone), (0, 255, 255), cv2.FILLED)
                    dir = 3

                elif center_x > int(width/2) + deadZone:
                    cv2.putText(imgContour, "GO RIGHT", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 3)
                    cv2.rectangle(imgContour, (int(width / 2) + deadZone, int(height / 2 - deadZone)),
                                  (int(width / 2) + deadZone, int(height / 2) + deadZone), (0, 255, 255), cv2.FILLED)

                    dir = 2
                else:
                    dir = 0

                cv2.line(imgContour, (int(width/2), int(height/2)), (center_x, center_y), (0, 0, 255),3)

    def display(img):
        cv2.line(img, (int(width/2 + deadZone), 0),(int(width/2 + deadZone), height), (255,0,0), 5)
        cv2.line(img, (int(width / 2 - deadZone), 0), (int(width / 2 - deadZone), height), (255, 0, 0), 5)
        cv2.line(img, (0, int(height/2 + deadZone)), (width, int(height/2 + deadZone)), (255, 0, 0), 5)
        cv2.line(img, (0, int(height/2 - deadZone)), (width, int(height/2 - deadZone)), (255, 0, 0), 5)
        cv2.circle(img, (int(width/2), int(height/2)), 5, (255,0,0), 5)





    while (1):
        f = me.get_frame_read()
        my_frame = f.frame
        img = cv2.resize(my_frame, (width, height))

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
        result = cv2.bitwise_and(img, img, mask=mask)

        imgB = cv2.GaussianBlur(result, (7, 7), 1)
        imgGray = cv2.cvtColor(imgB, cv2.COLOR_BGR2GRAY)

        threshold1 = cv2.getTrackbarPos("T_Hold1", "Params")
        threshold2 = cv2.getTrackbarPos("T_Hold2", "Params")
        imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
        imgDil = cv2.dilate(imgCanny, np.ones((5, 5)), iterations=1)

        imgConts = img.copy()

        getCountours(imgDil, imgConts)


        display(imgConts)

        if startCount == 0:
            me.takeoff()
            startCount = 1

        if dir == 1:
            me.yaw_velocity = -40
            print("LEFT")
        elif dir == 2:
            print("RIGHT")
            me.yaw_velocity = 40
        elif dir == 3:
            me.up_down_velocity = 40
            print("UP")
        elif dir == 4:
            me.up_down_velocity = -40
            print("DOWN")
        else:
            me.for_back_velocity = 0
            me.left_right_velocity = 0
            me.up_down_velocity = 0
            me.yaw_velocity = 0
            print("NOTHING")

        dir = 0
        if me.send_rc_control:

            me.send_rc_control(me.left_right_velocity, me.for_back_velocity, me.up_down_velocity, me.yaw_velocity)
            print("yaw_vel",  me.yaw_velocity, "up_down = ", me.up_down_velocity)
            print(me.get_battery())


        cv2.imshow("a",  img)
        cv2.imshow("2", result)
        cv2.imshow("6", imgConts)




        if cv2.waitKey(5) == 27:
            me.land()
            break
    cv2.destroyAllWindows()



if __name__ == '__main__':
    try:
        mainTello()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            me.land()
            me.land()
            me.land()
        except SystemExit:
            print("lol")
