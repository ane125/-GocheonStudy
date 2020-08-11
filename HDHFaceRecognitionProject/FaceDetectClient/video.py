# -*- coding: utf-8 -*-
"""
Created on Mon May 11 16:44:06 2020

@author: Handonghee
"""
import cv2
import FaceDetect_DNN
import FaceRecognition_LBPH

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from threading import Thread
from enum import Enum
import time

class Command(Enum):
     CamStart = 1
     FaceMode = 2
     CamStop = 3
        
class VideoController(QObject):
 
    sendImage = pyqtSignal(QImage)
    FaceDetect_DNN = None
    FR = None
    ModelPath = 'models/opencv_face_detector_uint8.pb'
    Configpath = 'models/opencv_face_detector.pbtxt'
    LBPHModelPath = 'TrainModel_100'
    
    FaceRectOffset = 20
    IsFaceMode = True    
    conf_threshold = 0.9
    
    
    Font = 2
    FaceThreshold = 130
    
    Red = (22,22,222)
    Green = (22,222,22)

    #Init
    def __init__(self, widget, size):
        super().__init__()
        self.widget = widget
        self.size = size
        self.sendImage.connect(self.widget.recvImage)        
        self.color = [QColor(255,0,0), QColor(255,128,0), QColor(255,255,0), QColor(0,255,0), QColor(0,0,255), QColor(0,0,128), QColor(128,0,128)]        
        self.initMudule()     
     
    #Command To VideoContoller     
    def CommandWork(self, InputCommand):
        if InputCommand is Command.CamStart:
            self.startCam()
        elif InputCommand is Command.CamStop:
            self.stopCam()
        elif InputCommand is Command.FaceMode:
            self.IsFaceMode = ~IsFaceMode
            
        self.WriteLog(InputCommand)
    
    #ConsolMethod
    def WriteLog(self, InputCommand):
        if InputCommand is Command.CamStart:
            print("Cam Start")
        elif InputCommand is Command.CamStop:
            print("Cam Stop")
        elif InputCommand is Command.FaceMode:
            print("FaceMode is " + str(self.IsFaceMode))
            
   
    #WorkMethod   
    def Workthread(self):
        while self.bThread:
            ok, frame = self.cap.read()
            if ok:                 
                if self.IsFaceMode is True:
                    frame = self.FaceRecognition(frame)
                                        
                self.sendImage.emit(self.CvToQImage(frame))
            else:
                print('cam read errror')
 
            time.sleep(0.01)

       
    def FindEvent(self, info):
        return info
    
    #FaceRecognition 
    def FaceRecognition(self,srcimg):
        self.FaceDetect_DNN.FindFace(srcimg)
        h, w, _ = srcimg.shape 
                
        detections = self.FaceDetect_DNN.Result
       
        # processing
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > self.conf_threshold:
                x1 = int(detections[0, 0, i, 3] * w) + self.FaceRectOffset
                y1 = int(detections[0, 0, i, 4] * h) + self.FaceRectOffset
                x2 = int(detections[0, 0, i, 5] * w) + self.FaceRectOffset
                y2 = int(detections[0, 0, i, 6] * h) + self.FaceRectOffset
                
                if x1 < 0 or y1 < 0 or x2 > w or y2 > h:
                    continue
                
                SaveFaceImage = srcimg[y1:y2,x1:x2]
                
                try :
                    SaveFaceImage = cv2.resize(SaveFaceImage, dsize=(96, 96), interpolation=cv2.INTER_AREA)   
                    Name = ' '
                    Value = 0 
                    Name, Value = self.FR.RecogFace(SaveFaceImage)
                    
                    if(Value < self.FaceThreshold):    
                        cv2.rectangle(srcimg, (x1, y1), (x2, y2), self.Green, int(round(h/150)), cv2.LINE_AA)                     
                        cv2.putText(srcimg, Name + ' : ' + str(round(Value,2)), (x1,y2+(self.Font * 10)), cv2.FONT_HERSHEY_PLAIN, self.Font ,self.Green,2, cv2.LINE_AA)
                    else:
                        cv2.rectangle(srcimg, (x1, y1), (x2, y2), self.Red, int(round(h/150)), cv2.LINE_AA)
                        cv2.putText(srcimg, 'Unknown : ' + str(round(Value,2)), (x1,y2+(self.Font * 10)), cv2.FONT_HERSHEY_PLAIN, self.Font ,self.Red,2, cv2.LINE_AA)  
                    
                    print('Find Face')
                except Exception as ex: # 에러 종류
                    print('에러가 발생 했습니다', ex)

        return srcimg
    
    #CamStart
    def startCam(self):
        try:
            self.cap = cv2.VideoCapture(0)
        except Exception as e:
            print('Cam Error : ', e)
        else:
            self.bThread = True
            self.thread = Thread(target=self.Workthread)
            self.thread.start()
            
    #CamStop      
    def stopCam(self):        
        self.bThread = False
        bopen = False
        try:
            bopen = self.cap.isOpened()
        except Exception as e:
            print('Error cam not opened')
        else:
            self.cap.release()
            
    #Init FaceDetectClass
    def initMudule(self):        
        self.FaceDetect_DNN = FaceDetect_DNN.FaceDetectDNN()        
        self.FaceDetect_DNN.conf_threshold = self.conf_threshold       
        self.FaceDetect_DNN.LoadModel(self.ModelPath, self.Configpath)
        self.FR = FaceRecognition_LBPH.FaceRecognition_LBPH()
        self.FR.ReadModel(self.LBPHModelPath)
        
    #CvToQImage  
    def CvToQImage(self,cvimage):
        rgb = cv2.cvtColor(cvimage, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytesPerLine = ch * w
        img = QImage(rgb.data, w, h, bytesPerLine, QImage.Format_RGB888)
        return img.scaled(self.size.width(), self.size.height(), Qt.KeepAspectRatio) 