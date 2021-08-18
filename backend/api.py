import time
from flask import Flask, Response, request
import cv2
import threading


app = Flask(__name__)

# initialize a lock used to ensure thread-safe
# exchanges of the frames (useful for multiple browsers/tabs
# are viewing tthe stream)
#lock = threading.Lock()
#camera = cv2.VideoCapture(0)

@app.route('/detect', methods = ['POST'])
def detect():
   if (request.files):
      file = request.files.get('image')
      #file = request.files['image']
      image = cv2.imdecode(file)
      print("hier")
      cv2.imshow('image window', image)
      cv2.waitKey(0)
   #camera = cv2.VideoCapture(0)
   #ret, frame = camera.read()
   #(flag, encodedImage) = cv2.imencode(".jpg", frame)
   #image = b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n'
   return {"whatever"}

# @app.route('/stream',methods = ['GET'])
# def stream():
#    return Response(generate(), mimetype = "multipart/x-mixed-replace; boundary=frame")

# def generate():
#    # grab global references to the lock variable
#    global lock
#    # initialize the video stream
#    camera = cv2.VideoCapture(0)
   
#    # check camera is open
#    if camera.isOpened():
#       rval, frame = camera.read()
#    else:
#       rval = False

#    # while streaming
#    while rval:
#       # wait until the lock is acquired
#       with lock:
#          # read next frame
#          rval, frame = camera.read()
#          # if blank frame
#          if frame is None:
#             continue

#          # encode the frame in JPEG format
#          (flag, encodedImage) = cv2.imencode(".jpg", frame)

#          # ensure the frame was successfully encoded
#          if not flag:
#             continue

#       # yield the output frame in the byte format
#       yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')
#    # release the camera
#    camera.release()

if __name__ == '__main__':
   host = "127.0.0.1"
   port = 5000
   debug = False
   options = None
   app.run(host, port, debug, options)