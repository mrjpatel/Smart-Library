# USAGE
# With default parameters
#         python3 02_encode.py
# OR specifying the dataset, encodings and detection method
#         python3 02_encode.py -i dataset -e encodings.pickle -d hog

# Acknowledgement
# This code is adapted from:
# https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/

# import the necessary packages
from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os


class ImageEncoding:

    def encode(self, encoding_file):
        print("Encoding registered face...")

        imagePaths = list(paths.list_images("dataset"))

        knownEncodings = []
        knownNames = []

        print("Started Processing images. Please wait")
        for (i, imagePath) in enumerate(imagePaths):
            name = imagePath.split(os.path.sep)[-2]

            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            boxes = face_recognition.face_locations(rgb, model="hog")
            encodings = face_recognition.face_encodings(rgb, boxes)

            for encoding in encodings:
                knownEncodings.append(encoding)
                knownNames.append(name)

        print("Finished Processing images!")
        print("Serializing encodings...")
        data = {
            "encodings": knownEncodings,
            "names": knownNames
            }

        with open(encoding_file, "wb") as f:
            f.write(pickle.dumps(data))
