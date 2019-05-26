# Acknowledgement
# This code is adapted from:
# https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/
#
# Code snippets use in this Module is taken from PIoT Course Tutorial 9
from imutils.video import VideoStream
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2


class FaceLogin:
    """
    Class for recognising user through facial recognition.
    It is used to recognise based on encoded data
    """

    def recognise(self):
        """
        Starts Video stream and checks detected face againist encoded data
        to recognise user through face.
        :return: The reognised user's username
        :rtype: str
        """
        data = pickle.loads(open("encodings.pickle", "rb").read())
        print("starting video stream...")

        # initialize the video stream and allow the camera sensor to warm up
        vs = VideoStream(src=0).start()
        time.sleep(2.0)

        # grab the frame from the threaded video stream
        frame = vs.read()

        # convert the input frame from BGR to RGB then resize it to have
        # a width of 750px (to speedup processing)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb = imutils.resize(frame, width=240)

        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input frame, then compute
        # the facial embeddings for each face
        boxes = face_recognition.face_locations(rgb, model="hog")
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []

        # loop over the facial embeddings
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(
                data["encodings"], encoding)
            name = "Unknown"

            if True in matches:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                    # determine the recognized face with the largest number
                    # of votes (note: in the event of an unlikely tie Python
                    # will select first entry in the dictionary)
                    name = max(counts, key=counts.get)

                names.append(name)

        for name in names:
            vs.stop()
            return(name)

        vs.stop()
        return ""
