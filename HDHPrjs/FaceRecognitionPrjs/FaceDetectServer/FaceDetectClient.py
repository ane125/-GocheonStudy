import sys
import os
import csv
import ServerClass
import threading 
from socket import *

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("Client.ui")[0]
t =[]

class Server(threading.Thread):
    def __init__(self,socket):
        super().__init__()
        self.s_socket = socket
    
        
    def run(self):
        self.c_socket, addr = self.s_socket.accept()
        print(addr[0],addr[1],"이 연결되었습니다")
        create_thread(self.s_socket)
        ThreadStaff=threading.Thread(target=self.c_recv)
        ThreadStaff.deamon=True
        ThreadStaff.start()
    
    def c_recv(self):
        while True:
            get_data=self.c_socket.recv(1024)
            print(get_data.decode('utf-8'))
            
    def c_send(self, put_data):
        self.c_socket.send(put_data.encode('utf-8'))
          

def create_thread(s_socket):
    print('Call Create Thread')
    index = len(t)
    t.append(Server(s_socket))
    t[index].deamon=True
    t[index].start()     
    
    
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

       
    serverSocket = 0
    
    def ServerOpen(self):
        text, ok = QInputDialog.getText(self, 'Server setting', 'Input port:')

        if ok:
            
            self.serverSocket = socket(AF_INET, SOCK_STREAM)
            ufsize=1024
            host='192.168.0.109'
            port=5001
            self.serverSocket.bind((host,port))
            self.serverSocket.listen(1)

            create_thread(self.serverSocket)

            self.LOGVIEWER.appendPlainText('Server open!')
            self.LOGVIEWER.appendPlainText('port : '+str(text))
            
    def ServerClose(self):
        reply = QMessageBox.question(self, 'Server close', 'Are you sure to close?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.LOGVIEWER.appendPlainText('Server close')
            for j in t:
                try:
                    j.c_socket.close()
                except:
                    pass
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