import cv2
import cv2.cv as cv
import numpy as np
import datetime

scale = 1
delta = 0
ddepth = cv2.CV_16S

cap = cv2.VideoCapture(0)

while(True):
	# capture frame-by-frame
	ret, frame = cap.read()
	#our operations on the frame come here
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# Display the resulting frame
	cv2.imshow('frame',frame)
	k = cv2.waitKey(1)
	if k % 256 == 27:
		break
	elif k % 256 == ord('s'):
 
		print str(datetime.datetime.now())
		filetime = str(datetime.datetime.now())
		filename = 'picture_' + filetime +'.png' # creates a filename which can be reused in the next lines of code
		cv2.imwrite(filename,frame)
		img = cv2.imread(filename,0)
		img = cv2.GaussianBlur(img,(3,3),0)
		#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

		# Gradient-X
		grad_x = cv2.Sobel(gray,ddepth,1,0,ksize = 3, scale = scale, delta = delta,borderType = cv2.BORDER_DEFAULT)
		#grad_x = cv2.Scharr(gray,ddepth,1,0)

		# Gradient-Y
		grad_y = cv2.Sobel(gray,ddepth,0,1,ksize = 3, scale = scale, delta = delta, borderType = cv2.BORDER_DEFAULT)
		#grad_y = cv2.Scharr(gray,ddepth,0,1)

		abs_grad_x = cv2.convertScaleAbs(grad_x)   # converting back to uint8
		abs_grad_y = cv2.convertScaleAbs(grad_y)

		dst = cv2.addWeighted(abs_grad_x,0.5,abs_grad_y,0.5,0)
		#dst = cv2.add(abs_grad_x,abs_grad_y)

		cv2.imshow('detected circles', dst)
		cv2.imwrite('picture_sobel' + filetime +'.png',dst)

cv2.waitKey(0)
cv2.destroyAllWindows()
