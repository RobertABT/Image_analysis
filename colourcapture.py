import numpy as np
import cv2
import datetime

# loading in a colour image as greyscale (could help see edges?)
cap = cv2.VideoCapture(1)

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
		cv2.imwrite('picture_' + str(datetime.datetime.now())+'.png',frame)

		

#when everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
