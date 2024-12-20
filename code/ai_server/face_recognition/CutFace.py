from config import EnvConfig
#import dlib
import cv2
import random
from ultralytics import YOLO

class CutFace():
    def __init__(self):
        self.env = EnvConfig()
        #face detector
        #if self.env.cut_face_model_name == 'yolo_face':
        self.detector = YOLO(self.env.yolo_face_model_path)
        #else:
        #    self.detector = dlib.get_frontal_face_detector() #2024.11.15 dlib offline
        
        
    def detector_face(self,pic_img):
        faces = []
        gray_img = cv2.cvtColor(pic_img, cv2.COLOR_BGR2GRAY)
        detect_f = self.detector(gray_img)
        for _ in detect_f:
            faces.append([_.left(), _.top(), _.width(), _.height()])
        return faces
    
    def cut_faces_from_img(self,pic_img): #BGR img
        face_boxes = []
        face_imgs = []
        
        
        #if self.env.cut_face_model_name == 'yolo_face':  ##2024.11.15 dlib offline 
        yolo_res = self.detector.predict(pic_img,stream=False,device='cuda:0',verbose=False) #verbose=False 关闭yolo回显    
        all_res = yolo_res[0].boxes.data.cpu().numpy()
    
        for face in all_res:
            if face[4] > 0.7 :
                x = int(max(0,face[0]))
                y = int(max(0,face[1]))
                w = int(min(pic_img.shape[1] - x, face[2]-face[0]))
                h = int(min(pic_img.shape[0] - y,face[3]-face[1]))
                face_imgs.append(pic_img[y:y+h, x:x+w])
                face_boxes.append([x,y,w,h])
        ##2024.11.15 dlib offline
        '''
        else:
        
            # 检测人脸
            faces = self.detector_face(pic_img)
            
            for face in faces:
                # 提取人脸区域
                #x, y, w, h = face.left(), face.top(), face.width(), face.height()
                x, y, w, h = face
                # Ensure that the region does not exceed the bounds of pic_img
                x = max(0, x)
                y = max(0, y)
                w = min(w, pic_img.shape[1] - x)
                h = min(h, pic_img.shape[0] - y)
            
                face_imgs.append(pic_img[y:y+h, x:x+w])
                face_boxes.append([x,y,w,h])
        '''
        
        return face_boxes,face_imgs

    def get_face_boxes(self,pic_img): #BGR img
        face_indexs = []
        #face_imgs = []
        
        #if self.env.cut_face_model_name == 'yolo_face': ##2024.11.15 dlib offline 
        yolo_res = self.detector.predict(pic_img,stream=False,device='cuda:0',verbose=False) #verbose=False 关闭yolo回显    
        all_res = yolo_res[0].boxes.data.cpu().numpy()

    
        for face in all_res:
            if face[4] > 0.7 :
                x = int(max(0,face[0]))
                y = int(max(0,face[1]))
                w = int(min(pic_img.shape[1] - x, face[2]-face[0]))
                h = int(min(pic_img.shape[0] - y,face[3]-face[1]))
                #face_imgs.append(pic_img[y:y+h, x:x+w])
                face_indexs.append([x,y,w,h])
        
        ##2024.11.15 dlib offline            
        '''
        else:
            # 检测人脸
            faces = self.detector_face(pic_img)

            for face in faces:
                # 提取人脸区域
                #x, y, w, h = face.left(), face.top(), face.width(), face.height()
                x, y, w, h = face
                # Ensure that the region does not exceed the bounds of pic_img
                x = max(0, x)
                y = max(0, y)
                w = min(w, pic_img.shape[1] - x)
                h = min(h, pic_img.shape[0] - y)
            
                #face_imgs.append(pic_img[y:y+h, x:x+w])
                face_indexs.append([x,y,w,h])
        '''
        
        return face_indexs#,face_imgs

    def mark_face_in_img(self,pic_img,name_face_dict):
        for dict_key in name_face_dict.keys():
            x,y,w,h = name_face_dict[dict_key]['face_index']
            name = name_face_dict[dict_key]['name']
            
            if name==self.env.defeat_match_name:
                mark_color = self.env.fixed_unrecognize_color
            else:
                if self.env.FACE_MARK_color_random:
                    mark_color = tuple((random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)))
                else:
                    mark_color = self.env.fixed_recognize_color
            
            
            cv2.rectangle(pic_img, (x, y), (x+w, y+h), mark_color, self.env.face_line_width)
            #cv2.putText(pic_img, name, (x, y-self.env.face_line_width), cv2.FONT_HERSHEY_SIMPLEX, self.env.text_size, mark_color, self.env.face_name_size)
        
        #print (pic_img.shape)
        return pic_img   
    
    
    
if __name__ == "__main__":
    testpic = r"F:\workspace\majun\img\majun.png"
    cut_face = CutFace()
    pic_img = cv2.imread(testpic)
    face_boxes,face_imgs = cut_face.cut_faces_from_img(pic_img)
    print (face_boxes)
    print (face_imgs)
        