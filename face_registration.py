# USAGE
# With default parameter of user/id
#       python3 01_capture.py -n default_user
# OR specifying the dataset and user/id
#       python3 02_capture.py -i dataset -n default_user

# Acknowledgement
# This code is adapted from:
# https://www.hackster.io/mjrobot/real-time-face-recognition-an-end-to-end-project-a10826

# import the necessary packages
import cv2
import os
from image_encoding import ImageEncoding


class FaceRegistration:

    def register(self, name):
        folder = "./dataset/{}".format(name)

        if not os.path.exists(folder):
            os.makedirs(folder)

        cam = cv2.VideoCapture(0)
        cam.set(3, 640)
        cam.set(4, 480)

        face_detector = cv2.CascadeClassifier(
            "haarcascade_frontalface_default.xml")

        img_counter = 0
        while img_counter <= 4:
            key = input(
                "Press e to cancel face regstration or ENTER to continue: ")
            if key == "e":
                return False

            ret, frame = cam.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)

            if(len(faces) == 0):
                print("No face detected, please try again")
                continue

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                img_name = "{}/{:04}.jpg".format(folder, img_counter)
                cv2.imwrite(img_name, frame[y:y + h, x:x + w])
                print("{} written!".format(img_name))
                img_counter += 1

        cam.release()
        print("Successfully! Registered face")
        return True
