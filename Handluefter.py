from cvzone.HandTrackingModule import HandDetector
import cv2
import serial
import time
import math

esp32 = serial.Serial(port='COM6', baudrate=115200, timeout=.1)

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.9, maxHands=1)

def write_read(x):
    esp32.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = esp32.readline()
    return data

while True:
    success, img = cap.read()
    
    hands, img = detector.findHands(img)
    
    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]
        
        x1, y1 = lmList1[8][0], lmList1[8][1]
        x2, y2 = lmList1[4][0], lmList1[4][1]
        
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        fan_speed = int(min(distance * 5, 255))

        print(f"Distance: {distance} Fan Speed: {fan_speed}")
        
        write_read(str(fan_speed))
    
    cv2.imshow("Image", img)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()