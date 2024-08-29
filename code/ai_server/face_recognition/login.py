
from config import EnvConfig
from FaceMatch import FaceMatch
from CutFace import CutFace
from utils import ImageArray2Cv2Image

import os
import cv2
import uuid
import numpy as np

class LogIn():
    def __init__(self):
        self.face_m = FaceMatch()
        self.env = EnvConfig()
        self.cut_tool = CutFace()
        
        self.students = set([])
        self.people_dict = {}
        
        self.info_prepare()
    
    
    def check_students_change(self):
        this_students = os.listdir(self.env.login_students_path)
        return self.students!=set(this_students)
    
    def info_prepare(self):
        if not self.check_students_change():
            return
        
        ## data clear
        self.students = set([])
        self.person_login_imgs_pth = {}
        
        
        self.load_student_login_info() 
        ###### begin prepare for body analyze #########
        #self.save_student_db_face_feature()
        #self.create_person_image_pth()   
    
    def load_student_login_info(self):
        this_students = os.listdir(self.env.login_students_path)
        self.students = set(this_students)
        ###
        self.people_dict = {}
        for student in self.students:
            student_img = cv2.imread(os.path.join(self.env.login_students_path,student))
            face_boxes,face_imgs = self.cut_tool.cut_faces_from_img(student_img)   
            for _ in range(len(face_boxes)):
                this_face_id = uuid.uuid1()
                self.people_dict[this_face_id] = {}
                self.people_dict[this_face_id]['name'] = student.rsplit('.')[0] if self.env.name_with_out_suffix else student
                self.people_dict[this_face_id]['face_index'] = face_boxes[_]
                self.people_dict[this_face_id]['face_img'] = face_imgs[_]
                #self.people_dict[this_face_id]['feature'] = self.face_m.get_img_feature(face_imgs[_])
                self.people_dict[this_face_id]['feature'] = self.face_m.get_img_vggface_feature(face_imgs[_])
    
    #def process(self,frame: np.ndarray):
    def process(self,capture_img):
        #capture_img = ImageArray2Cv2Image(frame)
        #cv2.imshow('prime_img',capture_img)
        self.info_prepare()
        #result_name_list = []
        target_face_boxes = self.cut_tool.get_face_boxes(capture_img)          
        result_dict = {}
        for _ in range(len(target_face_boxes)):
            this_face_id = uuid.uuid1()
            result_dict[this_face_id] = {}
            result_dict[this_face_id]['face_index']=target_face_boxes[_]
            x,y,w,h = target_face_boxes[_]
            name = self.face_m.face_imgs_select(capture_img[y:y+h, x:x+w],self.people_dict)
            result_dict[this_face_id]['name'] = name
            #result_name_list.append(name)
            
            #if self.env.SAVE_LOGIN_IMG:
            #    if name!= self.env.defeat_match_name:
            #        self.save_person_login_image(time_stamp,name,capture_img) #save full img for body detector
        #return self.cut_tool.mark_face_in_img(frame,result_dict),result_name_list
        #return self.cut_tool.mark_face_in_img(np.array(capture_img),result_dict),result_name_list, result_dict
        return self.cut_tool.mark_face_in_img(np.array(capture_img),result_dict), result_dict
    
if __name__ == "__main__":
    login = LogIn()
    print(login.people_dict)
    
    testpic = r"F:\workspace\majun\img\majun.png"
    pic_img = cv2.imread(testpic)
    
    result_img,name = login.process(pic_img)
    
    cv2.imshow('login',result_img)
    cv2.waitKey(3)
    print (name)