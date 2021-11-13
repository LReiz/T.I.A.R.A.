import numpy as np
import cv2
import serial

port = 'com5'
try:
	ArduinoSerial = serial.Serial(port, 9600, timeout=0.1)
	print('Arduino found')
except:
	print('Arduino not found. Try another port')
	ArduinoSerial = False

if ArduinoSerial:
	capture = cv2.VideoCapture(0)
	face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
	eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
	i = 0
	while True:
		ret, frame = capture.read()
		eyesFound = '0'

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.05, 5)
		print('frame ' + str(i))
		for (x, y, w, h) in faces:
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 200), 5)
			roi_gray = gray[y:y+h, x:x+w]
			roi_color = frame[y:y+h, x:x+w]
			eyes = eye_cascade.detectMultiScale(roi_gray, 1.05, 5)
			if len(eyes) > 1:
				eyesFound = '1'
				for (ex, ey, ew, eh) in eyes:
					cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 200, 0))

		if(ArduinoSerial):
			ArduinoSerial.write(eyesFound.encode('utf-8'))

		i += 1
		cv2.imshow('frame', frame)
		if cv2.waitKey(1) == ord('q'):
			break

	capture.release()
	cv2.destroyAllWindows()

