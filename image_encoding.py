# Acknowledgement
# This code is adapted from:
# https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/
#
# Code snippets use in this Module is taken from PIoT Course Tutorial 9
from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os


class ImageEncoding:
    """
    Class for encoding new images of user.
    It is used to encode images of user and store to encoding file
    """

    def encode(self, encoding_file):
        """
        Encode's users images
        :param encoding_file: the fike to encode image data to.
        :type encoding_file: str
        """
        print("Encoding registered face...")

        imagePaths = list(paths.list_images("dataset"))

        knownEncodings = []
        knownNames = []

        print("Started Processing images. Please wait")
        for (i, imagePath) in enumerate(imagePaths):
            name = imagePath.split(os.path.sep)[-2]

            # load the input image and convert it from RGB (OpenCV ordering)
            # to dlib ordering (RGB)
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input image
            boxes = face_recognition.face_locations(rgb, model="hog")
            encodings = face_recognition.face_encodings(rgb, boxes)

            for encoding in encodings:
                # add each encoding+name to our set of known names and encoding
                knownEncodings.append(encoding)
                knownNames.append(name)

        print("Finished Processing images!")
        print("Serializing encodings...")

        # dump the facial encodings + names to disk
        data = {
            "encodings": knownEncodings,
            "names": knownNames
            }

        with open(encoding_file, "wb") as f:
            f.write(pickle.dumps(data))
