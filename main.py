#1. get cam feed
#2. get faces
#3. realize faces
#4. For unknown face send zapier notification

# import the necessary packages
import os
import numpy as np
import argparse
import cv2
import face_recognition as fr

knownEncodings = [] 
knownNames = []

def initialize():
	cwd = os.getcwd()
	cwd += '/images/'
	for f in listdir(cwd):
		if isfile(join(cwd, f)):
			knownNames.append(os.path.splitext(os.path.basename(f))[0])
			faceLocation = fr.face_locations(f)
			knownEncodings.append(fr.face_encodings(f, faceLocation))

def stageOne():
	# construct the argument parse and parse the arguments
	initialize()
	cap = cv2.VideoCapture(0)
	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
	while cap.isOpened():
		_, img = cap.read()
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.1, 4)
		for(x,y,w,h) in faces:
			cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 3)
		cv2.imshow('img', img)
		stageTwo(img)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	cap.release()

def stageTwo(img):
	feedimg_location = fr.face_locations(img)
	feedimg_encoding = fr.face_encodings(img, feedimg_location)
	for dbimg_encoding in knownEncodings:
		match = face_recognition.compare_faces(dbimg_encoding, feedimg_encoding)
		distance = face_recognition.face_distance(dbimg_encoding, feeding_encoding)
		best = np.argmin(distance)
		if match[best]:
			name = knownNames[best]

if __name__ == "__main__":
	stageOne();
	stageTwo();