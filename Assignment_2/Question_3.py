#Q3.Show a vertically flipped frame after every 5 seconds using time.time(),from live webcam feed.
import cv2
import time
start_time=time.time()
cap= cv2.VideoCapture(0)
while True:
        x, frame= cap.read()
        flipped= cv2.flip(frame,-1) 
        end_time=time.time()
        diff=int(end_time-start_time)
        if diff%5==0:
            cv2.imshow("Frame",flipped)
        else:
            cv2.imshow("Frame",frame)
         
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break 
