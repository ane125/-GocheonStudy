import sys
import os
import csv
import threading 
from socket import *

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("Client.ui")[0]
t=[]

class Server(threading.Thread):
    def __init__(self,socket, windowClass):
        super().__init__()
        self.s_socket = socket
        self.windowClass = windowClass
    
  
    def run(self):
        self.c_socket, addr = self.s_socket.accept()
        self.windowClass.AddLogData(str(addr[0])+str(addr[1])+"이 연결되었습니다")

        create_thread(self.s_socket, self.windowClass)
        ThreadStaff=threading.Thread(target=self.c_recv)
        ThreadStaff.deamon=True
        ThreadStaff.start()
    
    def c_recv(self):
        while True:
            get_data=self.c_socket.recv(1024)
            self.windowClass.AddLogData(get_data.decode('utf-8'))
            
    def c_send(self, put_data):
        self.c_socket.send(put_data.encode('utf-8'))
          

def create_thread(s_socket, windowClass):
    print('Call Create Thread')
    index = len(t)
    t.append(Server(s_socket, windowClass))
    t[index].deamon=True
    t[index].start()     
    
   
#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :

    serverSocket =  socket(AF_INET, SOCK_STREAM)
   
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
        
        #Client Control Box
        self.BUTTON_SEND.clicked.connect(self.OnSendCommand)
        
        #Tool Button
        self.NETWORK_SERVEROPEN.triggered.connect(self.ServerOpen)
        self.NETWORK_SERVERCLOSE.triggered.connect(self.ServerClose)
        #self.LEARN_IMAGE.triggered.connect(self.LearnImageFunction)
        #self.LEARN_MAKECSV.triggered.connect(self.Makecsvfile)
        #self.LEARN_GetFaceImages.triggered.connect(self.ExtractFaceImage)
        #self.CAM_PLAY.triggered.connect(self.CamStart)
        #self.CAM_STOP.triggered.connect(self.CamStop)

       
    def OnSendCommand(self):
        message = str(self.LINEEDIT_SENDMESSAGE.text())
        self.AddLogData('send message : ' + str(message))
        
        for clientSocket in t:
            try:     
                clientSocket.c_send(message)
            except:
                pass   
  
        
    def AddLogData(self, msg):
        self.LOGVIEWER.appendPlainText(msg)
        
    def ServerOpen(self):
        inputPort, ok = QInputDialog.getText(self, 'Server setting', 'Input port:')

        if ok:
        
            ufsize=1024
            host='192.168.0.109'
            port=int(inputPort)
            self.serverSocket.bind((host,port))
            self.serverSocket.listen(1)

            create_thread(self.serverSocket,self)

            self.LOGVIEWER.appendPlainText('Server open!')
            self.LOGVIEWER.appendPlainText('ip : ' + str(host) + ' port : '+ str(port))
            
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
                
            self.serverSocket.close()
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