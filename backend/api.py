
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

med_list_name = [
  ["Dragee_blau", 20],
  ["Dragee_pink", 40],
  ["Kapsel_weiss", 35],
  ["kapsel_weiss_gelb", 50],
  ["Kapsel_weiss_gelb_orange", 40],
  ["Tablette_beige_oval", 100],
  ["Tablette_blau_rund", 55],
  ["Tablette_braun_rund", 50],
  ["Tablette_weiss_10mm", 40],
  ["Tablette_weiss_8mm", 25],
  ["Tablette_weiss_7mm", 60],
  ["Tablette_weiss_Zink", 70],
  ["Tablette_weiss_oval", 85],
  ["Weichkapsel_braun", 90],
  ["Weichkapsel_transparent", 120]
]

time_taken = ['morgens', 'mittags', 'abends', 'nachts']

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

barcodeData = "Patient1"
@app.route('/getGroundTruth', methods = ['POST', 'GET'])
def getGroundTruth():
   global barcodeData
   print(barcodeData)
   # if (request.files['image']):
   #    # print("hier")
   #    file = request.files['image']
   #    #file = request.files['image']
   #    image = Image.open(file)
   #    image = image.convert('RGB')
   #    image = numpy.array(image)
   #    image = image[:, :, ::-1].copy()
   #    #cv2.imwrite("testing.jpg", image)
   #    barcodes = pyzbar.decode(image)
   #    # barcodeData="PatientID"
   #    for barcode in barcodes:
   #       barcodeData = barcode.data.decode("utf-8")
   #       barcodeType = barcode.type
   #       print(barcodeData)
      
   with open(f"saved_data/{barcodeData}/Planung/plan.txt", "r") as f:
    
      lines = f.readlines()
   lines = [line.replace("\n", "") for line in lines]
   lines = [line.replace(" ", "") for line in lines]
   result = []
   #print(lines)
   for line in lines:
      med = line.split(",")
      #print(med)
      med[0] = med_list_name[int(med[0])][0]
      med[1] = int(med[1])
      med[2] = time_taken[int(med[2])]
      med.append(True)
      result.append(med)
   return { "groundtruth": result, "patientID":barcodeData}

@app.route('/detectMed', methods = ['POST', 'GET'])
def detectMed():

   global barcodeData
   print(barcodeData)
   med_result_folder = "data/io/result/med"
   for f in os.listdir(med_result_folder):
      os.remove(os.path.join(med_result_folder, f))

   processImage.run_pipeline_live()
   med_file_names = sorted((os.listdir(med_result_folder)))

   med_detected = 0
   medBox = []
   for file in med_file_names:
      if ".txt" in file:
         with open(os.path.join(med_result_folder, file)) as f:
            lines = f.readlines()
         med_list = []
         for line in lines:
            text_splits = line.split()
            #print(text_splits)
            available = False
            #box = {}
            for each_med in med_list:
               if text_splits[0] == each_med["id"]:
                  current_dose = each_med["dose"]
                  each_med["dose"] += current_dose
                  available = True
            if not available:
               med = {}
               med["id"] = int(text_splits[0])
               med["percent"] = float(text_splits[5])
               med["dose"] = med_list_name[int(text_splits[0])][1]
               med_list.append(med)
         med_detected = med_detected + len(med_list)
         medBox.append(med_list)
   
   ground_truth = []
   with open(f"saved_data/{barcodeData}/Planung/plan.txt", "r") as f:
      lines = f.readlines()
      lines = [line.replace("\n", "") for line in lines]
      lines = [line.replace(" ", "") for line in lines]
      #print(lines)
      for line in lines:
         med = line.split(",")
         #print(med)
         med = [int(e) for e in med]
         med.append(False)
         ground_truth.append(med)
   all_correct = True
   for med in ground_truth:
      for detected in medBox[med[2]]:
         if detected['id'] == med[0] and detected['dose'] == med[1]:
            med[3] = True
   # print(medBox)
   # print(ground_truth)
   for med in ground_truth:
      all_correct = all_correct and med[3]
      med[0] = med_list_name[med[0]][0]
      med[2] = time_taken[med[2]]
   message = ""
   if all_correct:
      message = "All medicines are correct"
   else:
      message = "There is misplaced medicine"
   if med_detected != len(ground_truth):
      return {"error": "The amount of med detected not match ground truth"}
   return { "prediction": ground_truth, "message": message, "correct": all_correct}

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
   #print(fileName, data)
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
