
from flask import Flask, Response, request
import cv2
from PIL import Image
import numpy

app = Flask(__name__)

@app.route('/detect', methods = ['POST', 'GET'])
def detect():
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
   return {"data": "whatever"}


if __name__ == '__main__':
   host = "127.0.0.1"
   port = 5000
   debug = False
   options = None
   app.run(host, port, debug, options)