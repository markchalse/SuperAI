

class EnvConfig:
    def __init__(self):
        self.platform = "LAPTOP"#"QT"#"LAPTOP"#"QT"#"LAPTOP" # "QT"

        
        #login
        if self.platform == "LAPTOP":
            self.ASR_MODEL_PATH = r"F:\workspace\majun\zhiyuanchuang_space\model_endpoints\voice_word\speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch"
            self.ASR_LOG_PATH = r"F:\workspace\majun\img\ASR.LOG"
        elif self.platform == "QT":
            self.ASR_MODEL_PATH = r"G:\workspace\majun\models\super_ai\voice_word\speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch"
            self.ASR_LOG_PATH = r"G:\workspace\majun\temp\ASR.LOG"
        
        
        #thread controler
        self.ai_online_flag = 'ai_super_online'
        self.server_online_flag = 'ai_asr_online'
        self.server_activate_flag = 'ai_asr_activate'
        
        
        #main redis
        
        self.redis_sound_flag = 'ai_asr_sound'
        self.redis_text_flag = 'ai_asr_text'
        
        
        #redis tools
        self.MAX_LEN = 3