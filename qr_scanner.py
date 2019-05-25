from imutils.video import VideoStream
from pyzbar import pyzbar
import datetime
import imutils
import time
import cv2


class QrScanner:
    @staticmethod
    def get_qr_codes():
        # initialize the video stream and allow the camera sensor to warm up
        print("Starting QR Scanner...")
        vs = VideoStream(src=0).start()
        time.sleep(2.0)
        found = set()
        i = 0
        # loop over the frames from the video stream
        while i < 10:
            # grab the frame from the threaded video stream and resize it to
            # have a maximum width of 400 pixels
            frame = vs.read()
            frame = imutils.resize(frame, width=400)

            # find the barcodes in the frame and decode each of the barcodes
            barcodes = pyzbar.decode(frame)

            # loop over the detected barcodes
            for barcode in barcodes:
                # convert the barcode data to string
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type

                #  print it and update the set
                if barcodeData not in found:
                    print("Found Barcode: {}".format(barcodeData))
                    found.add(barcodeData)

            # return if found a barcode
            if found:
                vs.stop()
                return found

            # wait a little before scanning again
            time.sleep(1)
            i += 1

        # close the output CSV file do a bit of cleanup
        print("Cannot Detect Barcode!")
        vs.stop()

if __name__ == "__main__":
    found = QrScanner.get_qr_codes()
    print(found)
