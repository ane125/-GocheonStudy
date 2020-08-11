import cv2
import FaceDetect_DNN
import FaceRecognition_LBPH
import time


ModelPath = 'models/opencv_face_detector_uint8.pb'
Configpath = 'models/opencv_face_detector.pbtxt'
    
FaceDetect_DNN = FaceDetect_DNN.FaceDetectDNN()
       
conf_threshold = 0.9
        
FaceDetect_DNN.conf_threshold = conf_threshold
       
FaceDetect_DNN.LoadModel(ModelPath, Configpath)

LBPHModelPath = 'TrainModel_100'
FR = FaceRecognition_LBPH.FaceRecognition_LBPH()
FR.ReadModel(LBPHModelPath)
Font = 2
FaceThreshold = 110

Red = (22,22,222)
Green = (22,222,22)

def DetectProcess(TempImg, Index):       
    
    FaceDetect_DNN.conf_threshold = conf_threshold       
        
    FaceDetect_DNN.FindFace(TempImg)
        
    h, w, _ = TempImg.shape 
                
    detections = FaceDetect_DNN.Result
    offset = 30
        # postprocessing
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * w)
            y1 = int(detections[0, 0, i, 4] * h)
            x2 = int(detections[0, 0, i, 5] * w)
            y2 = int(detections[0, 0, i, 6] * h)
            x1 += offset   
            x2 += offset
                            
            SaveFaceImage = TempImg[y1:y2,x1:x2]
                
            try :
                SaveFaceImage = cv2.resize(SaveFaceImage, dsize=(96, 96), interpolation=cv2.INTER_AREA)   
                #cv2.imwrite('Test' + str(Index) + '.jpg', SaveFaceImage)
                Name = ' '
                Value = 0 
                Name, Value = FR.RecogFace(SaveFaceImage)
                
                if(Value < FaceThreshold):    
                    cv2.rectangle(TempImg, (x1, y1), (x2, y2), Green, int(round(h/150)), cv2.LINE_AA)                     
                    cv2.putText(TempImg, Name + ' : ' + str(round(Value,2)), (x1,y2+(Font * 10)), cv2.FONT_HERSHEY_PLAIN, Font ,Green,2, cv2.LINE_AA)
                else:
                    cv2.rectangle(TempImg, (x1, y1), (x2, y2), Red, int(round(h/150)), cv2.LINE_AA)
                    cv2.putText(TempImg, 'Unknown : ' + str(round(Value,2)), (x1,y2+(Font * 10)), cv2.FONT_HERSHEY_PLAIN, Font ,Red,2, cv2.LINE_AA)  
                
                print('Find Face')
            except Exception as ex: # 에러 종류
                print('에러가 발생 했습니다', ex)
                                    
            # draw rects
            
            #cv2.putText(TempImg, '%.2f%%' % (confidence * 100.), (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            
            
                
          
# cap 이 정상적으로 open이 되었는지 확인하기 위해서 cap.isOpen() 으로 확인가능
cap = cv2.VideoCapture(0)

# cap.get(prodId)/cap.set(propId, value)을 통해서 속성 변경이 가능.
# 3은 width, 4는 heigh

print('width: {0}, height: {1}'.format(cap.get(3),cap.get(4)))

cap.set(3,1000)
cap.set(4,1000)

Index = 0
     
 
 
# 작업 코드
 
 

while(True):
    # ret : frame capture결과(boolean)
    # frame : Capture한 frame
    ret, frame = cap.read()

    if (ret):
        # image를 Grayscale로 Convert함.
        start = time.time()  # 
        DetectProcess(frame, Index)
        print("time :", time.time() - start) 
        Index += 1
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        
cap.release()
cv2.destroyAllWindows()