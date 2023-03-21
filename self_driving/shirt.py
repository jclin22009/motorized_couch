import numpy as np
import cv2

LOW = np.array([0, 80, 20])
HIGH = np.array([50, 255, 120])

def track_shirt(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    mask = cv2.inRange(img, LOW, HIGH)
    contours, hierarchies = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    blank = np.zeros(mask.shape[:2], dtype='uint8')

    cx, cy, w, h = 0, 0, 0, 0
    if len(contours) != 0:
        # cv2.drawContours(img, contours, -1, 255, 3)
        c = max(contours, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)
        cx = x + int(w/2)
        cy = y + int(h/2)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.circle(img, (cx, cy), 20, (0, 0, 255), -1)
        cv2.putText(img, "center", (cx - 100, cy - 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 5)
    
    img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
    return img, cx, cy, w, h