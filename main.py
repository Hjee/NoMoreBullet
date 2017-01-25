# main.py

from flask import Flask, render_template, Response
from camera import VideoCamera
import cv2
import numpy as np
from threading import Thread
cameraFrame = []
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def genTab(camera):
    global cameraFrame
    while True:
        cameraFrame.append(camera.get_frame())
        if len(cameraFrame) > 60 :
            #cameraFrame.pop(0)
          

def gen(camera):
    global cameraFrame
    while True:
        #frame = camera.get_frame()
        print(len(cameraFrame))
        if len(cameraFrame) !=0 :

            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + cameraFrame.pop() + b'\r\n\r\n')

@app.route('/video_feed/<feedNum>')
def video_feed(feedNum):
    print("video feed "+ feedNum)
    return Response(gen(VideoCamera(feedNum)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video_feed_late/<feedNum>')
def video_feed_late(feedNum):
    t = Thread(target=genTab, args=(VideoCamera(feedNum),))
    #genTab(VideoCamera(feedNum))
    return Response(gen(VideoCamera(feedNum)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/screen/<feedNum>')
def screen(feedNum):
    img = VideoCamera(feedNum)
    toto = b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + img.get_frame() + b'\r\n\r\n'
    return Response(toto,
                    mimetype='multipart/x-mixed-replace; boundary=frame')
					
					
@app.route('/disa')
def dispa():
    img1 = VideoCamera(1)
    img0 = VideoCamera(0)
    retval,imgA = img0.get_raw_frame()
    retvalo,imgB = img1.get_raw_frame()
    imageB = cv2.cvtColor(imgA,cv2.COLOR_BGR2GRAY)
    imageA = cv2.cvtColor(imgB,cv2.COLOR_BGR2GRAY)
    stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
    disparity = stereo.compute(imageA,imageB)
    ret, jpeg = cv2.imencode('.jpg', disparity)
    toto = b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n'
    return Response(toto,
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0',threaded=True)
