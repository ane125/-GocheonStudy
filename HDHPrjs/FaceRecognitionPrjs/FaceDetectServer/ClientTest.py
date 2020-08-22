# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 21:01:24 2020

@author: gkseh
"""

import time
from socket import *

port = 5001

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('192.168.0.109', port))

print('접속 완료')

while True:
    sendData = input()
    print('Send Data')
    clientSock.send(sendData.encode('utf-8'))
    data = clientSock.recv(1024)
    print('Received Data', repr(data))