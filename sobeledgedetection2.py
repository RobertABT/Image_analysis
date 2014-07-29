import cv2
import cv2.cv as cv
import numpy as np
from Tkinter import Tk
from tkFileDialog import askopenfilename
import math
import datetime

def isInCircle(x,y, circle):
	dist = math.sqrt((math.pow(x-int(circle[0]),2))+(math.pow(y-int(circle[1]),2)))
	if dist <= int(100): #limit radius to 100
		return True
	else:
		cv2.circle(original,(x,y),1,(255,255,255))
		return False

scale = 1
delta = 0
ddepth = cv2.CV_16S

GreyCirclePixel = [] #this creates an array which will store greyed pixel data
ColourCirclePixel = [] #this creates an array which will store coloured pixel data


while True:
	Tk().withdraw()
	filename = askopenfilename()
	print filename
	img = cv2.imread(filename)
	original = cv2.imread(filename,1)
	height, width, depth = img.shape
	print height
	print width
	img = cv2.GaussianBlur(img,(3,3),0)
	grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

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
#	cv2.imwrite('img',img)

	circles = cv2.HoughCircles(dst,cv.CV_HOUGH_GRADIENT,1,350,
				param1=50,param2=30,minRadius=100,maxRadius=0) #change to min=140 max=200 if needed
	print circles
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
#					print x,y
					ColourPixel = original[y,x] #this is normally a trip up point unless the image is read [y,x]
					GreyPixel = grey[y,x]
					GreyCirclePixel.append((x,y,GreyPixel))
					ColourCirclePixel.append((x,y,ColourPixel))
					pixelCount +=1
		AvgGreyCount = 0
		BlueAvgColourCount = 0
		GreenAvgColourCount = 0
		RedAvgColourCount = 0
		for i in range(0,pixelCount):
			AvgGreyCount += GreyCirclePixel[i][2]
			BlueAvgColourCount += ColourCirclePixel[i][2][0]
			GreenAvgColourCount += ColourCirclePixel[i][2][1]
			RedAvgColourCount += ColourCirclePixel[i][2][2]
		print 'Number of pixels within the circle detected=' #helps explain in terminal			
		print pixelCount
		AvgGreyCount = float(AvgGreyCount) / float(pixelCount) #divides the total of greypixel values by pixel count
		BlueAvgColourCount = float(BlueAvgColourCount) / float(pixelCount)
		GreenAvgColourCount = float(GreenAvgColourCount) / float(pixelCount)
		RedAvgColourCount = float(RedAvgColourCount) / float(pixelCount)
		fo = open('exportdata.txt', "a")
		fo.write(filename + '\n')
		fo.write( 'AvgColourCount(B,G,R)=' + '\n' + str(BlueAvgColourCount) + ' ' + str(GreenAvgColourCount) + ' ' + str(RedAvgColourCount) + '\n')
		fo.write( 'AvgGreyCount=' + '\n' + str(AvgGreyCount) + '\n' + '\n' )
		print 'AvgColourCount(B,G,R)='		
		print BlueAvgColourCount,GreenAvgColourCount,RedAvgColourCount 
		print 'AvgGreyCount=' 
		print AvgGreyCount 
		cv2.imshow('detected pixels', original)
		k = cv2.waitKey(0)
		if k % 256 == 27:
			cv2.destroyAllWindows()
			break
		elif k % 256 ==ord('s'):
			filetime = str(datetime.datetime.now())
			cv2.imwrite('detected pixels'+ filetime +'.png',original)
			break
		else:
			pass
cv2.destroyAllWindows()
