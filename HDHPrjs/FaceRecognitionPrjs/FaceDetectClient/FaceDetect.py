import cv2
   
class FaceDetect :
    
    eye_cascade = 0
    face_cascade = 0
    Image = 0
    
    def LearnEye(self, XmlPath):
        self.eye_cascade = cv2.CascadeClassifier(XmlPath)
                 
    def LearnFace(self, XmlPath):
        self.face_cascade = cv2.CascadeClassifier(XmlPath)
    
    def InputImage(self, Img):
        self.Image = Img
        
    def GetFaces(self, ScaleFactor, MinNeightbors):    
        
        Gray = cv2.cvtColor(self.Image,cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(Gray,ScaleFactor,MinNeightbors)
        return faces
    


