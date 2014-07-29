import cv2.cv as cv
import cv2
import numpy as np
from Tkinter import Tk
from tkFileDialog import askopenfilename

Tk().withdraw()
filename = askopenfilename()
img = cv2.imread(filename,0)
img = cv2.medianBlur(img,5)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
cannyimg=cv2.Canny(img,100,200)	

circles = cv2.HoughCircles(cannyimg,cv.CV_HOUGH_GRADIENT,1,20,
				param1=50,param2=30,minRadius=0,maxRadius=0) # if circles are too small change min to any number (in pixels)
if circles ==None:
	print 'No circles'
else:
	circles = np.uint16(np.around(circles))
	for i in circles[0,:]:
		#draw the outer circle
		cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
		#draw centre of the circle
		cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

cv2.imshow('detected circles', cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()
