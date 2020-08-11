import sys
import FaceDetect_DNN
import cv2
import os
import csv
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("Client.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    
    cvImg = None
    FaceDetect_DNN = None
    ModelPath = 'models/opencv_face_detector_uint8.pb'
    Configpath = 'models/opencv_face_detector.pbtxt'
    Index = 0
    ImageSize = [0.2,0.5,0.7,0.9,1.0]
    
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        
        #slider   
        self.FACEDETECTHSLIDER_FACETHREAHOLD.valueChanged.connect(self.FaceThresholdChangedFuncion)
     
        self.InitHorizonSlider()
        
        #ComboBox
        self.COMBOBOX_IMAGESIZE.currentIndexChanged.connect(self.ImageSizeChangedFuncion)
        
        #Tool Button
        self.FILE_LOADIMAGE.triggered.connect(self.LoadImageFunction)
        self.FILE_SAVEIMAGE.triggered.connect(self.SaveImageFunction)
        self.LEARN_IMAGE.triggered.connect(self.LearnImageFunction)
        self.LEARN_MAKECSV.triggered.connect(self.Makecsvfile)
        self.LEARN_GetFaceImages.triggered.connect(self.ExtractFaceImage)
        #FaceDetect 
        if(self.initMudule() is True):
            print("InitModule Success")
        else:
            print("InitModule Fail")
        
    #Init FaceDetect
    def initMudule(self):
       self.FaceDetect_DNN = FaceDetect_DNN.FaceDetectDNN()
       
       conf_threshold = self.FACEDETECTHSLIDER_FACETHREAHOLD.value() / 100
        
       self.FaceDetect_DNN.conf_threshold = conf_threshold
       
       Result = self.FaceDetect_DNN.LoadModel(self.ModelPath, self.Configpath)
       
       if(Result is False):
           print("ReadModel Fail")
           return False
       else:
           print("ReadModel Success")
           return True
             
    #ComboBoxChanged
    def ImageSizeChangedFuncion(self):  
        height, width , channel = self.cvImg.shape
        ImageWidth = int(width * self.ImageSize[self.COMBOBOX_IMAGESIZE.currentIndex()])
        ImageHieght = int(height * self.ImageSize[self.COMBOBOX_IMAGESIZE.currentIndex()])
        TempImg = cv2.resize(self.cvImg, dsize=(ImageWidth, ImageHieght), interpolation=cv2.INTER_AREA)          
        self.FaceDetect(TempImg)
        
        
    #FaceDetectProcess
    def FaceDetect(self, TempImg):        
        height, width , channel = self.cvImg.shape
        ImageWidth = int(width * self.ImageSize[self.COMBOBOX_IMAGESIZE.currentIndex()])
        ImageHieght = int(height * self.ImageSize[self.COMBOBOX_IMAGESIZE.currentIndex()])
        
        TempImg = cv2.resize(self.cvImg, dsize=(ImageWidth, ImageHieght), interpolation=cv2.INTER_AREA)          
        
        if(TempImg is None or self.FaceDetect_DNN is None):
            return
                           
        self.DetectProcess(TempImg)       
        self.QPIXMAX_IMAGE.setPixmap(self.Cv2QPixMap(TempImg))  
       
    
    #DetectdPrcces
    def DetectProcess(self, TempImg):
                           
        conf_threshold = self.FACEDETECTHSLIDER_FACETHREAHOLD.value() / 100
        
        self.FaceDetect_DNN.conf_threshold = conf_threshold       
        
        self.FaceDetect_DNN.FindFace(TempImg)
        
        h, w, _ = TempImg.shape 
                
        detections = self.FaceDetect_DNN.Result
       
        # postprocessing
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > conf_threshold:
                x1 = int(detections[0, 0, i, 3] * w)
                y1 = int(detections[0, 0, i, 4] * h)
                x2 = int(detections[0, 0, i, 5] * w)
                y2 = int(detections[0, 0, i, 6] * h)
                
                SaveFaceImage = TempImg[y1:y2,x1:x2]
                
                try :
                    SaveFaceImage = cv2.resize(SaveFaceImage, dsize=(96, 96), interpolation=cv2.INTER_AREA)   
                    cv2.imwrite('Test' + str(self.Index) + '.jpg', SaveFaceImage)
                    self.Index = self.Index + 1
                except Exception as ex: # 에러 종류
                    print('에러가 발생 했습니다', ex)
                    
                
                
                # draw rects
                cv2.rectangle(TempImg, (x1, y1), (x2, y2), (255, 255, 255), int(round(h/150)), cv2.LINE_AA)
                cv2.putText(TempImg, '%.2f%%' % (confidence * 100.), (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)                   
                
    
    
    #Cv2QPixMap
    def Cv2QPixMap(self, TempImg):
        TempImg = cv2.cvtColor(TempImg, cv2.COLOR_BGR2RGB)
        height, width, byteValue = TempImg.shape
        byteValue = byteValue * width       
        qImage = QImage(TempImg, width, height, byteValue, QImage.Format_RGB888)
        return QPixmap.fromImage(qImage)
    
    def LearnImageFunction(self) :
        fname = QFileDialog.getExistingDirectory()
        
        file_list = os.listdir(fname)
        tfr = TFRecordManager.TFRecordManager()
        
        for Image in file_list:
            LearnImage_Path = fname + '/' + Image           
            tfr.writeTFRecord(0, LearnImage_Path)
         
    #extract Face Image 
    def ExtractFaceImage(self):
        fname = QFileDialog.getExistingDirectory()
        
        file_list = os.listdir(fname)
        
        
        for Image in file_list:            
            if(Image[len(Image) - 3] is 'j'):          
                LearnImage_Path = fname + '/' + Image            
                self.cvImg = cv2.imread(LearnImage_Path) 
                
                TmpImg = self.cvImg.copy()
                self.FaceDetect(TmpImg)
                cv2.waitKey(10)
            
        print("Extract face process Success!")
            
    #Make csv file
    def Makecsvfile(self) :
        fname = QFileDialog.getExistingDirectory()
        
        file_list = os.listdir(fname)
        
        #파일 열기 
        #validationfile, trainfile
        f = open('validationfile.csv','a', newline='')
        wr = csv.writer(f)
        
        #파일 쓰기
        for Image in file_list:
            LearnImage_Path = fname + '/' + Image
            wr.writerow([LearnImage_Path, 'sulhyun', 5])
            
        f.close()
        print("Make csv process Success!") 
          
    #LoadImage
    def LoadImageFunction(self) :
   
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')   
        
        #-->Read Image with Opencv
        data = fname[0]      
        print(data)
        self.cvImg = cv2.imread(data) 
        
        if(self.cvImg is None):
            return
        
        TmpImg = self.cvImg.copy()
        self.FaceDetect(TmpImg)
             
     #SaveImage
    def SaveImageFunction(self) :
        print("Save")

        
    #Horizontal Slider
    def FaceThresholdChangedFuncion(self):               
        print(self.FACEDETECTHSLIDER_FACETHREAHOLD.value() / 100)
        
        if(self.cvImg is None):
            return
        
        TmpImg = self.cvImg.copy()
        self.FaceDetect(TmpImg)
               
         
   
    def InitHorizonSlider(self) :
        self.FACEDETECTHSLIDER_FACETHREAHOLD.setMaximum(100)
        self.FACEDETECTHSLIDER_FACETHREAHOLD.setMinimum(1)
                
        self.FACEDETECTHSLIDER_FACETHREAHOLD.setValue(70)
        
if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()