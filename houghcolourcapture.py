import numpy as np
import cv2
import cv2.cv as cv
import datetime

cap = cv2.VideoCapture(0) #this uses the first webcam on the system, change to (1) to use the second camera

while(True):
	# capture frame-by-frame
	ret, frame = cap.read()
	#our operations on the frame come here
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# Display the resulting frame
	cv2.imshow('frame',frame)
	k = cv2.waitKey(1)
	if k % 256 == 27: #ESC key quits
		break
	elif k % 256 == ord('s'): #s key saves
 
		print str(datetime.datetime.now())
		filetime = str(datetime.datetime.now()) #saves date-time of imagecapture
		filename = 'picture_' + filetime +'.png' # creates a filename which can be reused in the next lines of code
		cv2.imwrite(filename,frame)
		img = cv2.imread(filename,0)
		img = cv2.medianBlur(img,5)
		cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)	
                cannyimg=cv2.Canny(img,100,200)
		circles = cv2.HoughCircles(cannyimg,cv.CV_HOUGH_GRADIENT,1,350,
			   param1=50,param2=30,minRadius=140,maxRadius=200)
		if circles != None:
			circles = np.uint16(np.around(circles))
			for i in circles[0,:]:
				#draw the outer circle
				cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
				#draw centre of the circle
				cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
			cv2.imshow('detected circles',cimg)
			filename2 = 'picture_circles_' + filetime +'.png' #creates second file for treated image
			cv2.imwrite(filename2,cimg)
		else:
			print 'no circles' 
			pass

#when everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
