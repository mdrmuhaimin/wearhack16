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

WEB_CAM_INDEX = 0

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



# initialize the first frame in the video stream
firstFrame = None

# loop over the frames of the video
while True:
	# grab the current frame and initialize the occupied/unoccupied
	# text
	(grabbed, frame) = camera.read()
	text = "Unoccupied"

	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if not grabbed:
		break

	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=min(500, frame.shape[1]))
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # detect people in the image
	(rects, weights) = hog.detectMultiScale(frame, winStride=(4, 4),
		padding=(8, 8), scale=1.05)

	orig = frame.copy()

    # draw the original bounding boxes
	for (x, y, w, h) in rects:
		cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # apply non-maxima suppression to the bounding boxes using a
	# fairly large overlap threshold to try to maintain overlapping
	# boxes that are still people
	rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
	pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

	# draw the final bounding boxes
	for (xA, yA, xB, yB) in pick:
		cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)

	# # if the first frame is None, initialize it
	# if firstFrame is None:
	# 	firstFrame = gray
	# 	continue
    #
	# # compute the absolute difference between the current frame and
	# # first frame
	# frameDelta = cv2.absdiff(firstFrame, gray)
	# thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    #
	# # dilate the thresholded image to fill in holes, then find contours
	# # on thresholded image
	# thresh = cv2.dilate(thresh, None, iterations=2)
	# (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #
	# # loop over the contours
	# for c in cnts:
	# 	# if the contour is too small, ignore it
	# 	if cv2.contourArea(c) < args["min_area"]:
	# 		continue
    #
	# 	# compute the bounding box for the contour, draw it on the frame,
	# 	# and update the text
	# 	(x, y, w, h) = cv2.boundingRect(c)
	# 	cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
	# 	text = "Occupied"
    #
	# # draw the text and timestamp on the frame
	# cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
	# 	cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	# cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
	# 	(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    #
	# # show the frame and record if the user presses a key
	# cv2.imshow("Security Feed", frame)
	# cv2.imshow("Thresh", thresh)
	# cv2.imshow("Frame Delta", frameDelta)
	cv2.imshow("Pedestrian Detector", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
