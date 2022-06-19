import pyautogui as py
import cv2 as cv
import time
import numpy as np
import hand_tracking_module as htm
import math

cap = cv.VideoCapture(0)

#################################
wcam = 640
hcam = 480
wsch = 1920
hsch = 1080
clocx, plocx = 0, 0
clocy, plocy = 0, 0
smoothening = 5
#################################

ptime = 0
# initializing the hand tracking object
detector = htm.detector(max_hands=1)

while True:
    success, frame = cap.read()
    frame = detector.draw_hands(frame)
    # finding the position of all the fingers
    lm_list = detector.find_pos(frame)

    # Check how many fingers are up
    fingers = detector.fingers_up(thumb=True)

    # Creating a rectangle box to avoid the detection errors while going to the ends
    cv.rectangle(frame, (120, 40), (wcam - 50, 270), (255, 0, 255), thickness=1)

    if len(lm_list) != 0:
        # creating the variables for the position of the index and the middle finger
        x1, y1 = lm_list[8][1:]
        x2, y2 = lm_list[12][1:]

        # moving mode
        if fingers[1]:
            x3 = np.interp(x1, (120, wcam - 50), (0, wsch))
            y3 = np.interp(y1, (40, 270), (0, hsch))
            # Smoothening of the mouse
            clocx = plocx + (x3 - plocx) / (smoothening)
            clocy = plocy + (y3 - plocy) / (smoothening)

            py.moveTo(wsch - clocx, clocy)
            plocx, plocy = clocx, clocy

        # clicking mode
        if fingers[1] and fingers[2]:
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            cv.line(frame, (x1, y1), (x2, y2), (255, 0, 255), thickness=3)
            length = math.hypot(x2 - x1, y2 - y1)
            cv.circle(frame, (int(cx), int(cy)), 10, (0, 255, 0), thickness=cv.FILLED)
            # if length
            print(length)
            if length < 60:
                py.click()
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    cv.putText(frame, str(int(fps)), (50, 50), cv.FONT_ITALIC, 1, (0, 255, 0), thickness=1)
    cv.imshow("frame", frame)
    if cv.waitKey(1) & 0xFF == ord('d'):
        break
cap.release()
cv.destroyAllWindows()
