# -*- coding: utf-8 -*-
"""
Created on Sat May  9 18:45:28 2020

@author: Handonghee
"""
import cv2
import numpy as np
import os
from os import listdir
from os.path import isfile, join

class FaceRecognition_LBPH():
    models = []
    names = []
    
    def ReadModel(self, ModelPath):
        Model_list = os.listdir(ModelPath)
    
        for Model in Model_list:
            path = ModelPath + '/' + Model
            self.names.append(Model)
        
            readmodel = cv2.face.LBPHFaceRecognizer_create()
            readmodel.read(path)      
            self.models.append(readmodel)
        
    def RecogFace(self,Image):    
        #CvtImage BGR to Gray       
        face = cv2.cvtColor(Image, cv2.COLOR_BGR2GRAY)
    
        #read Model  
        i = 0
        ResultIndex = 0
        Min = 5000000
        Name = ''
        for predictmodel in self.models:
            result = predictmodel.predict(face)
            if(Min > result[1]):
                Min = result[1]
                ResultIndex = i               
            i = i + 1  
            
        return self.names[ResultIndex], Min