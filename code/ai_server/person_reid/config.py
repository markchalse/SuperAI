
class EnvConfig:
    def __init__(self,server='person_reid'):
        self.platform = "LAPTOP"#"QT"#"LAPTOP"#"QT"#"LAPTOP" # "QT"
        
        if self.platform == "LAPTOP":
            # body detector
            self.detector_model_path = r"D:\ai_space\model_endpoints\person_reid\detr_face_body.pt"
            # body feature
            self.reid_model_path = r"D:\ai_space\model_endpoints\person_reid\net_last.pth"
            # body feature path
            self.body_features_path = r"D:\ai_space\temp\person_reid\body_features"
            
        elif self.platform == "QT":
            # body detector
            self.detector_model_path = r"D:\ai_space\model_endpoints\person_reid\detr_face_body.pt"
            # body feature
            self.reid_model_path = r"D:\ai_space\model_endpoints\person_reid\net_last.pth"
            # body feature path
            self.body_features_path = r"D:\ai_space\temp\person_reid\body_features"      
            
        
        
        self.face_recognition_redis_key = '101_50_0'
        self.camera_redis_key = '101_3_0'#'101_1_0'
        self.person_reid_key = '101_51_0'
        
        
        #每个人最多有几个身体特征
        self.feature_max_count = 10
        
        
        
        # cv name print
        self.face_line_width = 25
        self.face_name_size = 5
        self.text_size = 2 #字体大小 1 2 3 4 5
        
        
        #thread controler
        self.ai_online_flag = 'ai_super_online'
        if server == 'person_reid':
            self.server_online_flag = 'ai_person_reid_online'
            self.server_activate_flag = 'ai_person_reid_activate'
        else:#feature collect
            self.server_online_flag = 'ai_feature_collect_online'
            self.server_activate_flag = 'ai_feature_collect_activate'
        