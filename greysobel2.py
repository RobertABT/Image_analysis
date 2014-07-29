import cv2
import cv2.cv as cv
import numpy as np
from Tkinter import Tk
from tkFileDialog import askopenfilename
import math
import datetime

def isInCircle(x,y, circle):
	dist = math.sqrt((math.pow(x-circle[0],2))+(math.pow(y-circle[1],2)))
	if dist <= int(100):
		return True
	else:
		cv2.circle(original,(x,y),1,(255,255,255))
		return False

scale = 1
delta = 0
ddepth = cv2.CV_16S

GreyCirclePixel = [] #this creates an array which will store greyed pixel data
ColourCirclePixel = [] #this creates an array which will store coloured pixel data

Tk().withdraw()
filename = askopenfilename()
img = cv2.imread(filename)
height, width, depth = img.shape
print height
print width
print 'please wait ~10 seconds'
original = cv2.imread(filename,1)
img = cv2.GaussianBlur(img,(3,3),0)
cv2.imwrite('img.png',img)
grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imwrite('grey.png',grey)
# Gradient-X
grad_x = cv2.Sobel(grey,ddepth,1,0,ksize = 3, scale = scale, delta = delta,borderType = cv2.BORDER_DEFAULT)
#grad_x = cv2.Scharr(grey,ddepth,1,0)
# Gradient-Y
grad_y = cv2.Sobel(grey,ddepth,0,1,ksize = 3, scale = scale, delta = delta, borderType = cv2.BORDER_DEFAULT)
#grad_y = cv2.Scharr(grey,ddepth,0,1)
abs_grad_x = cv2.convertScaleAbs(grad_x)   # converting back to uint8
abs_grad_y = cv2.convertScaleAbs(grad_y)

dst = cv2.addWeighted(abs_grad_x,0.5,abs_grad_y,0.5,0)
#dst = cv2.add(abs_grad_x,abs_grad_y)
cv2.imwrite('dst.png',dst)

circles = cv2.HoughCircles(dst,cv.CV_HOUGH_GRADIENT,1,350,
				param1=50,param2=30,minRadius=140,maxRadius=200) #change to min=140 max=200 if needed
if circles ==None:
	print 'No circles'
else:
	circles = np.uint16(np.around(circles))
	for i in circles[0,:]:
		#draw the outer circle
		cv2.circle(dst,(i[0],i[1]),i[2],(255,255,255),2)
		#draw centre of the circle
		cv2.circle(dst,(i[0],i[1]),2,(125,125,125),3)
cv2.imwrite('circles.png',dst)

if circles ==None:
	print 'No circles'
else:
	circles = np.uint16(np.around(circles))
	for i in circles[0,:]:
		#draw the outer circle
		cv2.circle(dst,(i[0],i[1]),i[2],(255,255,255),2)
		#draw centre of the circle
		cv2.circle(dst,(i[0],i[1]),2,(125,125,125),3)
	testcircle = circles[0][0] # the first circle
	pixelCount = 0
	for x in range(width):
		for y in range (height):
			if isInCircle(x,y,testcircle):
				print x,y
	#			pixel = original[x,y]
	#			print pixel
	#			newimg= cv2.circle(img,(x,y),1,(pixel))
				pixelCount +=1
	print pixelCount
	cv2.imshow('detected pixels', original)
	k = cv2.waitKey(0)
	if k==27:
		cv2.destroyAllWindows()
	elif k==ord('s'):
		filetime = str(datetime.datetime.now())
		cv2.imwrite('detected pixels'+ filetime +'.png',original)
