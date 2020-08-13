import sys
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

   
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        
        #regist Camera
        #self.videocontroller = VideoController(self, QSize(self.QPIXMAX_IMAGE.width(), self.QPIXMAX_IMAGE.height()))
        #slider   
        #self.FACEDETECTHSLIDER_FACETHREAHOLD.valueChanged.connect(self.FaceThresholdChangedFuncion)
     
        #self.InitHorizonSlider()
        
        #ComboBox
        #self.COMBOBOX_IMAGESIZE.currentIndexChanged.connect(self.ImageSizeChangedFuncion)
        
        #Tool Button
        self.NETWORK_SERVEROPEN.triggered.connect(self.ServerOpen)
        self.NETWORK_SERVERCLOSE.triggered.connect(self.ServerClose)
        #self.LEARN_IMAGE.triggered.connect(self.LearnImageFunction)
        #self.LEARN_MAKECSV.triggered.connect(self.Makecsvfile)
        #self.LEARN_GetFaceImages.triggered.connect(self.ExtractFaceImage)
        #self.CAM_PLAY.triggered.connect(self.CamStart)
        #self.CAM_STOP.triggered.connect(self.CamStop)

                  
    def ServerOpen(self):
        text, ok = QInputDialog.getText(self, 'Server setting', 'Input port:')

        if ok:
            self.LOGVIEWER.appendPlainText('Server open!')
            self.LOGVIEWER.appendPlainText('port : '+str(text))
            
    def ServerClose(self):
        reply = QMessageBox.question(self, 'Server close', 'Are you sure to close?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.LOGVIEWER.appendPlainText('Server close')
        else:
            self.LOGVIEWER.appendPlainText('Server continue')
            
            
  
if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()