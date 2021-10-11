
from flask import Flask, Response, request
import cv2
from PIL import Image
import numpy
from pyzbar import pyzbar
from flask import jsonify
import json
import os

app = Flask(__name__)

@app.route('/detect', methods = ['POST', 'GET'])
def detect():
   #print("hier")
   #print(request.files.to_dict())
   if (request.files['image']):
      file = request.files['image']
      #file = request.files['image']
      image = Image.open(file)
      image = image.convert('RGB')
      image = numpy.array(image)
      image = image[:, :, ::-1].copy() 
      cv2.imwrite("testing.jpg", image)
      barcodes = pyzbar.decode(image)
      barcodeData="test1"
      for barcode in barcodes:
         barcodeData = barcode.data.decode("utf-8")
         barcodeType = barcode.type
         #print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
      #print(barcodeData)
      filenames = os.listdir("saved_data")
      data = {}
      if barcodeData in filenames:
         with open(f"saved_data/{barcodeData}") as f:
            data = json.load(f)
      else:
         with open("saved_data/empty") as f:
            data = json.load(f)
   return {barcodeData: data}

@app.route('/detectPatientID', methods = ['POST', 'GET'])
def detectPatientID():
   print("hier")
   print(request.files.to_dict())
   if (request.files['image']):
      file = request.files['image']
      #file = request.files['image']
      image = Image.open(file)
      image = image.convert('RGB')
      image = numpy.array(image)
      image = image[:, :, ::-1].copy() 
      cv2.imwrite("testing.jpg", image)
      barcodes = pyzbar.decode(image)
      barcodeData="test1"
      for barcode in barcodes:
         barcodeData = barcode.data.decode("utf-8")
         #barcodeType = barcode.type
         #print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
      result = []
      print(barcodeData)
      # if barcodeData == "test1":
      #    box1 = ["med1", "med2"]
      #    box2 = ["med3", "med7"]
      #    box3 = ["med4", "med9"]
      #    box4 = ["med2", "med8"]
      #    box5 = ["med6", "med2"]
      # result.append(box1)
      # result.append(box2)
      # result.append(box3)
      # result.append(box4)
      # result.append(box5)   
   return {barcodeData: result}

@app.route('/saveData', methods = ['POST'])
def saveData():
   data = json.loads(request.data)
   #print(data["column-2"])
   print(data.keys())
   dictKeys = list(data.keys())
   fileName = dictKeys[0]
   with open(f'saved_data/{fileName}', 'w') as f:
      json.dump(data, f)
   return {"data": "everything good"}



if __name__ == '__main__':
   host = "127.0.0.1"
   port = 5000
   debug = False
   options = None
   app.run(host, port, debug, options)