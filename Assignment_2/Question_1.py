import cv2 
img = cv2.imread('Flower.jpeg')
print(img.shape) #gives us size of image 
a = int(input ("Enter first dimension"))
b = int(input ("Enter second dimension"))
cv2.line(img,(0,0),(b,a),(255,0,0),5)
cv2.imshow('frame',img)
cv2.waitKey(0)
