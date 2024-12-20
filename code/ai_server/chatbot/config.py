import os

class EnvConfig:
    def __init__(self):        
        self.chatbot_workspace = r"D:\ai_space\temp\chatbot"
        
        self.chatbot_log_path = os.path.join(self.chatbot_workspace,'CHATBOT.LOG')
        
        #thread controler
        self.ai_online_flag = 'ai_super_online'
        self.server_online_flag = 'ai_chatbot_online'
        self.server_activate_flag = 'ai_chatbot_activate'
        
        
        #main redis
        
        self.redis_ask_flag = 'ai_chatbot_ask'
        self.redis_answer_flag = 'ai_chatbot_answer'
        
        
        #redis tools
        self.MAX_LEN = 3
        
        #utils GLM
        #Kejiyun 5G
        #self.server_url = "http://192.168.161.241:5000/chat"
        
        #Readmi 5G
        self.server_url = "http://192.168.31.84:5000/chat"