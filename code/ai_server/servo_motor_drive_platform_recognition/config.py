import os

class EnvConfig:
    def __init__(self):
        self.platform = "LAPTOP"#"QT"#"LAPTOP"#"QT"#"LAPTOP" # "QT"
        

        #main 
        #self.chat_model_name = "BAIDU"#"GLM" #"BAIDU"#"GLM"#"BAIDU"#"GLM"  #"BAIDU"
        
        #login
        if self.platform == "LAPTOP":
            self.yolo_model_check_point = r"F:\majun\model_endpoints\servo_motor_drive_platform_recognition\majun_table.pt"
            self.camera_source_key = '101_1_0'
            
        elif self.platform == "QT":
            self.yolo_model_check_point = r"G:\workspace\majun\models\super_ai\servo_motor_drive_platform_recognition\majun_table.pt"
            self.camera_source_key = '101_1_1'
        
        #thread controler
        self.ai_online_flag = 'ai_super_online'
        self.server_online_flag = 'ai_smdpr_online'
        self.server_activate_flag = 'ai_smdpr_activate'
        

        
        #redis tools
        self.MAX_LEN = 10
        self.smpdr_result_key = '101_52_0'
        
        #object yolo confidence
        self.obj_confidence = 0.9