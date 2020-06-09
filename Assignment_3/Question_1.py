#Q1 Using loops, fill an image with randomly coloured, equal sized squares. Square dimensions:
#width = (image width)/7, height = (image height)/7.

import cv2
import random

img = cv2.imread ('image.jpg')
dimensions = img.shape
y = (img.shape[1])/7
x = (img.shape[0])/7

for b in range (1,8): #for rows
    
    x1 = int(x*(b-1))
    x2 = int(x*b)
    
    for a in range(1,8):  #for columns 

        y1 = int(y*(a-1))
        y2 = int(y*a)

        img[x1:x2,y1:y2] = (random.randint (0, 255), random.randint (0, 255), random.randint (0, 255))
        cv2.imshow ('frame', img)
    
cv2.waitKey(3000)
cv2.destroyWindow('frame')