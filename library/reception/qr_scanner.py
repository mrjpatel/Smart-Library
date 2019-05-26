# Acknowledgement
# This code is adapted from:
# https://www.pyimagesearch.com/2018/05/21/
# an-opencv-barcode-and-qr-code-scanner-with-zbar/
# and this code is adapted from TL10/QR_Scan/barcode_scanner_console.py


from imutils.video import VideoStream
from pyzbar import pyzbar
import datetime
import imutils
import time
import cv2
import json


class QrScanner:
    """
    Class for scanning the QR codes on the Reception Pi
    """
    @staticmethod
    def get_qr_codes():
        """Retrieves Data from QR Code.

        This function acitvates the camera and scans for QR codes
        It then inturpates the codes into a list and returns it
        """
        # initialize the video stream and allow the camera sensor to warm up
        print("Starting QR Scanner...")
        vs = VideoStream(src=0).start()
        time.sleep(2.0)
        found = list()
        i = 0
        print("Please Hold QR Code to the Camera")
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
                    found.append(json.loads(barcodeData))

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
