


class EnvConfig:
    def __init__(self):
        self.platform = "LAPTOP"#"QT"#"LAPTOP"#"QT"#"LAPTOP" # "QT"
        
        #login
        if self.platform == "LAPTOP":
            #self.tts_workspace = r"F:\workspace\majun\img\tts_files"
            self.tts_workspace = r"F:\majun\tmp\tts_files"
        elif self.platform == "QT":
            self.tts_workspace = r"G:\workspace\majun\temp\tts_files"
        
        #utils
        self.tts_model = 'edge' #pytts
        
        #thread controler
        self.ai_online_flag = 'ai_super_online'
        self.server_online_flag = 'ai_tts_online'
        self.server_activate_flag = 'ai_tts_activate'
        
        
        #main redis
        self.redis_text_flag = 'ai_tts_text'
        self.redis_sound_flag = 'ai_tts_sound'
        
        
        #redis tool
        self.REDIS_MAX_LEN = 5