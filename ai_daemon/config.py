import os

class EnvConfig:
    def __init__(self):
        self.platform = "LAPTOP"#"QT"#"LAPTOP"#"QT"#"LAPTOP" # "QT"
        
        #login
        if self.platform == "LAPTOP":
            self.codebase_path = r"F:\workspace\majun\zhiyuanchuang_space\ai_code\superai\SuperAI"
            
        elif self.platform == "QT":
            self.codebase_path = r"G:\workspace\majun\temp\chatbot"
        
        
        
        self.server_bat = {}
        self.server_bat['camera_sensor']=os.path.join(self.codebase_path,r'code\data_sensor\camera_sensor\script\camera_sensor_start.bat')
        self.server_bat['face_recognition']=os.path.join(self.codebase_path,r'code\ai_server\face_recognition\script\face_recognition_start.bat')
        self.server_bat['asr']=os.path.join(self.codebase_path,r'code\ai_server\voice_to_word\script\asr_start.bat')
        self.server_bat['tts']=os.path.join(self.codebase_path,r'code\ai_server\text_to_speech\script\tts_start.bat')
        self.server_bat['chatbot']=os.path.join(self.codebase_path,r'code\ai_server\chatbot\script\chatbot_start.bat')
        self.server_bat['feature_collect']=os.path.join(self.codebase_path,r'code\ai_server\person_reid\script\feature_collect_start.bat')
        self.server_bat['person_reid']=os.path.join(self.codebase_path,r'code\ai_server\person_reid\script\person_reid_start.bat')
        
        
        self.server_pid_key = 'ai_server_pid'
        
        self.ai_online_flag = 'ai_super_online'