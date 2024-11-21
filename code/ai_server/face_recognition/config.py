class EnvConfig:
    def __init__(self):
        #self.USE_MODEL = 'vggface' #senet50
        self.login_students_path = r"D:\ai_space\img\student"
            
        
        
        #main
        self.camera_img_list_redis_key = '101_3_0'#'101_1_0'#'101_3_0'#'101_1_0' #camera front    
        
            
        self.name_with_out_suffix = True  #没有后缀名
        self.defeat_match_name = 'UnKnow' #没匹配到人脸的情况 给的名字
        
        
        
        #cut face
        #self.cut_face_model_name = 'yolo_face' #'yolo_face'#'dlib' ##2024.11.15 dlib offline 
        self.yolo_face_model_path = r'D:\ai_space\model_endpoints\face_recognition\yolov8n-face.pt'
        self.facenet_model_path = r'D:\ai_space\model_endpoints\face_recognition\facenet_inception_resnetv1.pth'
        self.FACE_MARK_color_random = False  #每个人不同颜色
        self.fixed_recognize_color = (0,255,0)
        #self.fixed_unrecognize_color = (255,0,0) #rgb
        self.fixed_unrecognize_color = (0,0,255) #bgr
        self.face_line_width = 10  #25 2024.11.15
        self.face_name_size = 5
        self.text_size = 2 #字体大小 1 2 3 4 5
        
        
        #face match
        self.vggface_same_face_euler_distance_threshold =0.6 # 0.6       # [0,1] The closer to 0, the higher the accuracy
                                                                    #0.65 99% 45% 100%
                                                                    
                                                                    

        
        #thread controler
        self.ai_online_flag = 'ai_super_online'
        self.server_online_flag = 'ai_face_recognition_online'
        self.server_activate_flag = 'ai_face_recognition_activate'