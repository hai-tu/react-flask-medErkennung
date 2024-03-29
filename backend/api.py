
from flask import Flask, Response, request
import cv2
from PIL import Image
import numpy
from pyzbar import pyzbar
from flask import jsonify
import processImage
import json
import os

app = Flask(__name__)

@app.route('/detect', methods = ['POST', 'GET'])
def detect():
   if (request.files['image']):
      file = request.files['image']
      image = Image.open(file)
      image = image.convert('RGB')
      image = numpy.array(image)
      image = image[:, :, ::-1].copy()
      cv2.imwrite("testing.jpg", image)
      barcodes = pyzbar.decode(image)
      barcodeData="PatientID"
      for barcode in barcodes:
         barcodeData = barcode.data.decode("utf-8")
         barcodeType = barcode.type
         print(barcodeData)
         #print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
      filenames = os.listdir("saved_data")
      data = {}
      if barcodeData in filenames:
         with open(f"saved_data/{barcodeData}") as f:
            data = json.load(f)
      else:
         with open("saved_data/empty") as f:
            data = json.load(f)
   return {barcodeData: data}

def getAllMedID(medBox):
   result = []
   for med in medBox:
      result.append(med["id"])
   return result

@app.route('/detectMed', methods = ['POST', 'GET'])
def detectMed():
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
      barcodeData="PatientID"
      for barcode in barcodes:
         barcodeData = barcode.data.decode("utf-8")
         barcodeType = barcode.type
         print(barcodeData)
      test_folder = "data/io/in/test"
      for f in os.listdir(test_folder):
         os.remove(os.path.join(test_folder, f))
      savePath = os.path.join(test_folder, "testing.jpg")
      cv2.imwrite(savePath, image)

   result_folder = "data/io/result/med"
   for f in os.listdir(result_folder):
      os.remove(os.path.join(result_folder, f))
   processImage.run_pipeline_live()
   file_names = (os.listdir(result_folder))
   i = 1
   medBox = []
   for file in file_names:
      if ".txt" in file:
         with open(os.path.join(result_folder, file)) as f:
            lines = f.readlines()
         med_list = []
         for line in lines:
            text_splits = line.split()
            available = False
            #box = {}
            for each_med in med_list:
               if text_splits[0] == each_med["id"]:
                  each_med["amount"] += 1
                  available = True
            if not available:
               med = {}
               med["id"] = text_splits[0]
               med["percent"] = text_splits[5]
               med["amount"] = 1
               med_list.append(med)
            #boxID = "box_" + str(i)
            #box[boxID] = med

            #med_list.append(med)
         #fileName = "box" + str(i)
         #medBox[fileName] = med_list
         resultMed = {}
         resultMed["detectedMed"] = med_list
         resultMed["result"] = True
         medBox.append(resultMed)
         #medBox.append(med_list)
         i = i + 1
   print(medBox)
   with open(f"saved_data/{barcodeData}") as f:
      ground_truth = json.load(f)
   gtruth = []
   for value in ground_truth.values():
      box = []
      for med in value["taskIds"]:
         eachMed = {}
         medID = med["med"].split("-")[1]
         eachMed["id"] = str(int(medID) - 1)
         eachMed["amount"] = med["amount"]
         box.append(eachMed)
      gtruth.append(box)
   result = []
   for i in range(len(gtruth)):
      interResult = True
      if len(medBox[i]["detectedMed"]) != len(gtruth[i]):
         interResult = False
      else:
         for med in medBox[i]["detectedMed"]:
            if med["id"] not in getAllMedID(gtruth[i]):
               interResult = False
               #result.append(False)
            else:
               for each_med in gtruth[i]:
                  if each_med["id"] == med["id"]:
                     if med["amount"] != each_med["amount"]:
                        interResult = False

      result.append(interResult)
   #print("result is", result)
   print("Ground Truth", gtruth)
   for i, test in enumerate(result):
      medBox[i]["result"] = result[i]
   # print(gtruth)
   # print(ground_truth)
   return { "groundtruth": gtruth, "prediction": medBox, "result":result, "patientID":barcodeData}

@app.route('/saveData', methods = ['POST', 'GET'])
def saveData():
   data = json.loads(request.data)
   #print(data["column-2"])
   print(data.keys())
   dictKeys = list(data.keys())
   fileName = dictKeys[0]
   data = data[fileName]
   with open(f'saved_data/{fileName}', 'w') as f:
      json.dump(data, f)
   result = []
   for f in os.listdir("saved_data"):
      if f != "empty":
         result.append(f)
   return {"list": result}

@app.route('/getPatientID', methods = ['GET'])
def getPatientID():
   result = []
   for f in os.listdir("saved_data"):
      if f != "empty":
         result.append(f)
   return {"list": result}

@app.route('/loadPatientFile', methods = ['POST', 'GET'])
def loadPatientFile():
   jsonData = json.loads(request.data)
   fileName = jsonData["fileName"]
   data = ""
   with open(f"saved_data/{fileName}") as f:
            data = json.load(f)
   print(fileName, data)
   return {fileName: data}

@app.route('/deletePatientFile', methods = ['POST', 'GET'])
def deletePatientFile():
   jsonData = json.loads(request.data)
   files = jsonData["fileName"]
   result = []
   for file in os.listdir("saved_data"):
      if file not in files:# and file != "empty":
         result.append(file)
      else:
         os.remove(f"saved_data/{file}")
   return {"list": result}

if __name__ == '__main__':
   host = "127.0.0.1"
   port = 5000
   debug = False
   options = None
   app.run(host, port, debug, options)
