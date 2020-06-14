#Use two mouse clicks in the live video feed to define a template and track it in the
#frame (Live Video Feed).(Moderate)

import cv2
import numpy as np 

cap = cv2.VideoCapture(0)

pnts=[]

def mouse(event,x,y,flags,param):
    c=0
    if event==cv2.EVENT_LBUTTONDOWN:
        if c==0:
            c=c+1
            cv2.imwrite('image.jpg',frame)
        
        pnts.append((x,y))
        
while True:
    x,frame=cap.read()
    cv2.namedWindow('frame')
    cv2.setMouseCallback('frame',mouse)
    img=cv2.imread('image.jpg')
    
    if len(pnts)==2:
        cropped = img[pnts[0][1]:pnts[1][1],pnts[0][0]:pnts[1][0]]
        cv2.imshow('cropped', cropped)
        template_gray=cv2.cvtColor(cropped,cv2.COLOR_BGR2GRAY)
        width = cropped.shape[1]
        height = cropped.shape[0]
        img_gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        res=cv2.matchTemplate(img_gray,template_gray,cv2.TM_CCOEFF_NORMED)
        loc=np.where(res>=0.9)
        
        for x,y in zip(*loc[::-1]):
            cv2.rectangle(frame,(x,y),(x+width,y+height),(0,255,0),1)
            cv2.putText(frame,'Object',(x,y),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1)

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break 

cv2.namedWindow("frame")
cv2.setMouseCallback("frame",mouse)
cv2.destroyAllWindows()