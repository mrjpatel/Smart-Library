from imutils.video import VideoStream
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2


class FaceLogin:

    def __init__(self):
        data = pickle.loads(open("encodings.pickle", "rb").read())

    def recognise(self):
        print("starting video stream...")
        vs = VideoStream(src=0).start()
        time.sleep(2.0)

        frame = vs.read()

        # convert the input frame from BGR to RGB then resize it to have
        # a width of 750px (to speedup processing)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb = imutils.resize(frame, width=args["resolution"])

        boxes = face_recognition.face_locations(
                                            rgb,
                                            model=args["detection_method"]
                                            )
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []

        for encoding in encodings:
            matches = face_recognition.compare_faces(
                data["encodings"], encoding)
            name = "Unknown"

            if True in matches:
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                    name = max(counts, key=counts.get)

                names.append(name)

        for name in names:
            return(name)


if __name__ == "__main__":
    fl = FaceLogin()
    print(fl.recognise())
