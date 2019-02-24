import numpy as np
import cv2
import sys
import time

cap = cv2.VideoCapture(1)
inputImage = cv2.imread("download.png")

# Display barcode / QR code location
def display(im, bbox):
    n = len(bbox)
    for j in range(n):
        cv2.line(im, tuple(bbox[j][0]), tuple(bbox[ (j+1) % n][0]), (255, 0, 0), 3)
    # Display results
    cv2.imshow("Results", im)

qrDecoder = cv2.QRCodeDetector()

while True:
    data, bbox, rectifiedImage = qrDecoder.detectAndDecode(inputImage)
    if (len(data) > 0):
        print("Decoded data : {}".format(data))
        display(inputImage, bbox)
        rectifiedImage = np.uint8(rectifiedImage);
        cv2.imshow("Rectified QRCode", rectifiedImage);
    else:
        print("QR Code not detected")
        cv2.imshow("Results", inputImage)
    _, feed = cap.read()
    cv2.waitKey(0)
cv2.destroyAllWindows()