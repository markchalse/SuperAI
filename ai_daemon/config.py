import os

class EnvConfig:
    def __init__(self):
        self.platform = "QT"#"QT"#"LAPTOP"#"QT"#"LAPTOP" # "QT"
        
        #login
        if self.platform == "LAPTOP":
            self.codebase_path = r"F:\workspace\majun\zhiyuanchuang_space\ai_code\superai\SuperAI"
            
        elif self.platform == "QT":
            self.codebase_path = r"G:\workspace\majun\code\SuperAI"
        
        self.server_pid_key = 'ai_server_pid'
        self.ai_online_flag = 'ai_super_online'
        
        self.server_code_info = {}
        
        self.server_code_info['asr'] = {}
        self.server_code_info['asr']['start'] = os.path.join(self.codebase_path,r'code\ai_server\voice_to_word\script\asr_start.bat')
        self.server_code_info['asr']['online_flag'] = 'ai_asr_online'
        self.server_code_info['asr']['activate_flag'] = 'ai_asr_activate'
        
        self.server_code_info['chatbot'] = {}
        self.server_code_info['chatbot']['start'] = os.path.join(self.codebase_path,r'code\ai_server\chatbot\script\chatbot_start.bat')
        self.server_code_info['chatbot']['online_flag'] = 'ai_chatbot_online'
        self.server_code_info['chatbot']['activate_flag'] = 'ai_chatbot_activate'
        
        self.server_code_info['tts'] = {}
        self.server_code_info['tts']['start'] = os.path.join(self.codebase_path,r'code\ai_server\text_to_speech\script\tts_start.bat')
        self.server_code_info['tts']['online_flag'] = 'ai_tts_online'
        self.server_code_info['tts']['activate_flag'] = 'ai_tts_activate'
        
        
        
        self.server_code_info['camera_sensor'] = {}
        self.server_code_info['camera_sensor']['start'] = os.path.join(self.codebase_path,r'code\data_sensor\camera_sensor\script\camera_sensor_start.bat')
        #self.server_code_info['camera_sensor']['offline'] = os.path.join(self.codebase_path,r'code\data_sensor\camera_sensor\script\camera_sensor_down.bat')
        #self.server_code_info['camera_sensor']['activate'] = os.path.join(self.codebase_path,r'code\data_sensor\camera_sensor\script\camera_sensor_activate.bat')
        #self.server_code_info['camera_sensor']['deactivate'] = os.path.join(self.codebase_path,r'code\data_sensor\camera_sensor\script\camera_sensor_deactivate.bat')
        
        self.server_code_info['camera_sensor']['online_flag'] = 'ai_singal_camera_online'
        self.server_code_info['camera_sensor']['activate_flag'] = 'ai_singal_camera_activate'
        
        
        
        self.server_code_info['face_recognition'] = {}
        self.server_code_info['face_recognition']['start'] = os.path.join(self.codebase_path,r'code\ai_server\face_recognition\script\face_recognition_start.bat')
        self.server_code_info['face_recognition']['online_flag'] = 'ai_face_recognition_online'
        self.server_code_info['face_recognition']['activate_flag'] = 'ai_face_recognition_activate'
        
        
        self.server_code_info['camera_top'] = {}
        self.server_code_info['camera_top']['start'] = os.path.join(self.codebase_path,r'code\data_sensor\camera_sensor_top\script\camera_sensor_start.bat')
        self.server_code_info['camera_top']['online_flag'] = 'ai_singal_camera_top_online'
        self.server_code_info['camera_top']['activate_flag'] = 'ai_singal_camera_top_activate'
        
        
        self.server_code_info['platform_traj'] = {}
        self.server_code_info['platform_traj']['start'] = os.path.join(self.codebase_path,r'code\ai_server\platform_trajectory\script\smdpj_start.bat')
        self.server_code_info['platform_traj']['online_flag'] = 'ai_smdpj_online'
        self.server_code_info['platform_traj']['activate_flag'] = 'ai_smdpj_activate'
        
        self.server_code_info['smdpr'] = {}
        self.server_code_info['smdpr']['start'] = os.path.join(self.codebase_path,r'code\ai_server\servo_motor_drive_platform_recognition\script\smdpr_start.bat')
        self.server_code_info['smdpr']['online_flag'] = 'ai_smdpr_online'
        self.server_code_info['smdpr']['activate_flag'] = 'ai_smdpr_activate'
        
        
        self.server_code_info['score'] = {}
        self.server_code_info['score']['start'] = os.path.join(self.codebase_path,r'code\ai_server\score\script\score_start.bat')
        self.server_code_info['score']['online_flag'] = 'ai_score_online'
        self.server_code_info['score']['activate_flag'] = 'ai_score_activate'
        
        
        '''
        self.server_bat = {}
        self.server_bat['camera_sensor']=os.path.join(self.codebase_path,r'code\data_sensor\camera_sensor\script\camera_sensor_start.bat')
        #self.server_bat['face_recognition']=os.path.join(self.codebase_path,r'code\ai_server\face_recognition\script\face_recognition_start.bat')
        self.server_bat['asr']=os.path.join(self.codebase_path,r'code\ai_server\voice_to_word\script\asr_start.bat')
        self.server_bat['tts']=os.path.join(self.codebase_path,r'code\ai_server\text_to_speech\script\tts_start.bat')
        self.server_bat['chatbot']=os.path.join(self.codebase_path,r'code\ai_server\chatbot\script\chatbot_start.bat')
        #self.server_bat['feature_collect']=os.path.join(self.codebase_path,r'code\ai_server\person_reid\script\feature_collect_start.bat')
        #self.server_bat['person_reid']=os.path.join(self.codebase_path,r'code\ai_server\person_reid\script\person_reid_start.bat')
        '''
        self.server_pool = ['asr','tts','chatbot','camera_sensor','face_recognition','camera_top','platform_traj','smdpr','score']
        
        