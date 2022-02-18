from pyzbar import pyzbar
import argparse
import cv2

print(cv2.__version__)

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])

barcodes = pyzbar.decode(image)

for barcode in barcodes:
    (x, y, w, h) = barcode.rect
    cv2.rectangle(image, (x,y), (x+w, y+h), (0, 0, 255), 2)
    barcodeData = barcode.data.decode("utf-8")
    barcodeType = barcode.type
    # draw the barcode data and barcode type on the image
    text = "{} ({})".format(barcodeData, barcodeType)
    cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.5, (0, 0, 255), 2)
	# print the barcode type and data to the terminal
    print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
# show the output image
cv2.imshow("Image", image)
cv2.waitKey(0)

#detector = cv2.QRCodeDetector()
# detect and decode
#data, vertices_array, binary_qrcode = detector.detectAndDecode(image)
# if there is a QR code
# print the data
#cv2.imshow("image", image)
#cv2.waitKey(0)
#if vertices_array is not None:
  #print("QRCode data:")
  #print(data)
#else:
  #print("There was some error") 