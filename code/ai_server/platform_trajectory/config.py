import os

class EnvConfig:
    def __init__(self):
        self.platform = "LAPTOP"#"QT"#"LAPTOP"#"QT"#"LAPTOP" # "QT"
        
        
        
        #thread controler
        self.ai_online_flag = 'ai_super_online'
        self.server_online_flag = 'ai_smdpj_online'
        self.server_activate_flag = 'ai_smdpj_activate'
        

        
        #redis tools
        self.MAX_LEN = 10
        self.smpdr_result_key = '101_52_0'
        self.smpdj_result_key = 'ai_platform_trajectory_result'
        self.trajectory_id_key = 'ai_platform_trajectory_id'
        
        #object yolo confidence
        self.obj_confidence = 0.9