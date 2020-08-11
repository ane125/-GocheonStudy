# -*- coding: utf-8 -*-
"""
Created on Sat May  9 17:45:02 2020

@author: http://blog.naver.com/PostView.nhn?blogId=chandong83&logNo=221436424539&categoryNo=29&parentCategoryNo=0&viewDate=&currentPage=1&postListTopCurrentPage=1&from=postView
"""
import cv2
import numpy as np
import os
from os import listdir
from os.path import isfile, join


ModelName ='Handonghee'
Label = 3
__file__ = 'C:/Users/user/anaconda3/envs/FRFD'
ModelPath = 'C:/Users/user/anaconda3/envs/FRFD/TrainModel'
ImagePath = 'C:/Users/user/anaconda3/envs/FRFD/Imagecollection/Handonghee/Test503.jpg'

#faces폴더에 있는 파일 리스트 얻기 
data_path = __file__ + '/VALIDATION_DIR'

fname = data_path + '/' + ModelName

file_list = os.listdir(fname)

onlyfiles =[]        
        #파일 쓰기
for Image in file_list:
    LearnImage_Path = fname + '/' + Image
    onlyfiles.append(LearnImage_Path)
                           
#데이터와 매칭될 라벨 변수 
Training_Data, Labels = [], []
#파일 개수 만큼 루프 
for i, files in enumerate(onlyfiles):    
    image_path = onlyfiles[i]
    #이미지 불러오기 
    images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    #이미지 파일이 아니거나 못 읽어 왔다면 무시
    if images is None:
        continue    
    #Training_Data 리스트에 이미지를 바이트 배열로 추가 
    Training_Data.append(np.asarray(images, dtype=np.uint8))
    #Labels 리스트엔 카운트 번호 추가 
    Labels.append(Label)

#훈련할 데이터가 없다면 종료.
if len(Labels) == 0:
    print("There is no data to train.")
    exit()

#Labels를 32비트 정수로 변환
Labels = np.asarray(Labels, dtype=np.int32)
#모델 생성 
model = cv2.face.LBPHFaceRecognizer_create()
#학습 시작 
model.train(np.asarray(Training_Data), np.asarray(Labels))
model.save(ModelName)
print("Model Training Complete!!!!!")