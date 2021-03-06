# USAGE
# python motion_detector.py
# python motion_detector.py --video videos/example_01.mp4

# import the necessary packages
from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
import datetime
import time
import copy

# from flask import Flask
#
# app = Flask(__name__)
#
# @app.route("/")
# def hello():
#     return "Hello World!"
#
# if __name__ == "__main__":
#     app.run()

SCALE_VAL = 2.00
WEB_CAM_INDEX = 0
WIN_STRIDE_VAL = 4
NEAREST_POINT = 315
FRAME_WIDTH = 600

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

# we are reading from webcam
camera = cv2.VideoCapture(WEB_CAM_INDEX)

time.sleep(0.25)

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
# hog.setSVMDetector(cv2.HOGDescriptor_getPeopleDetector48x96())



# initialize the first frame in the video stream
firstFrame = None

# loop over the frames of the video
# grab the current frame and initialize the occupied/unoccupied
# text
(grabbed, frame) = camera.read()


# resize the frame, convert it to grayscale, and blur it
frame = imutils.resize(frame, width=min(FRAME_WIDTH, frame.shape[1]))

# detect people in the image
(rects, weights) = hog.detectMultiScale(frame, winStride=(WIN_STRIDE_VAL, WIN_STRIDE_VAL),
    padding=(8, 8), scale=SCALE_VAL)

orig = frame.copy()

# draw the original bounding boxes
for (x, y, w, h) in rects:
	if ( y + h ) < NEAREST_POINT:
		## Object is not in the collision zone
		cv2.rectangle(orig, (x, y), (x + w, y + h), (255, 0, 0), 2)
	else:
		## Object is in the collision zone
		cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 255, 0), 2)

# apply non-maxima suppression to the bounding boxes using a
# fairly large overlap threshold to try to maintain overlapping
# boxes that are still people
rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

# draw the final bounding boxes
for (xA, yA, xB, yB) in pick:
	if ( y + h ) < NEAREST_POINT:
		## Object is not in the collision zone
		cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
	else:
		## Object is in the collision zone
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

while True:
    cv2.imshow("Pedestrian Detector", frame)
    key = cv2.waitKey(1) & 0xFF


# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
