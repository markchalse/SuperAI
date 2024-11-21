


import os
import redis
import time

from config import EnvConfig
from thread_controller import ThreadControler
from redis_tools import *
from utils import *


class ChatModel:
    def __init__(self):
        self.glm_model = GLM()
        self.baidu_model = BaiduAI()
        self.model_name = "glm"
        
    def get_response(self,ask_text):
        if self.model_name == "glm":
            try:
                text = self.glm_model.get_response(ask_text)
            except Exception as e:
                print (e)
                self.model_name = "baidu"
                return False,""
        else:
            try:
                text = self.baidu_model.get_response(ask_text)
            except Exception as e:
                print (e)
                self.model_name = "glm"
                return False,""
        return True,text
        
        


if __name__ == "__main__":
    #asr_engine = AutomaticSpeechRecognition()
    chatbot_log = read_chatbot_log()
    # 初始化Redis连接  
    r = redis.Redis(host='localhost', port=6379, db=0)  
    
    print ('chat bot server online!')
    time.sleep(0.3)
    env = EnvConfig()
    
    
    chat_ai = ChatModel()
    
    tc = ThreadControler()
    tc.init_thread()
    
    pid = os.getpid()
    print(f"当前进程的PID是: {pid}")   
    push_server_pid(r,'ai_server_pid','chatbot',str(pid))
    
    print ('wait for activate...')
    
    
    while True:
        if not tc.check_activate():
            time.sleep(3)
        else:
            activate_step = 0
            
            print ('chat bot server activate!')
            
            while True:
                activate_step+=1 
                
                chat_ask_dicts = get_redis_chatbot(r,env.redis_ask_flag)
                chat_answer_dicts = get_redis_chatbot(r,env.redis_answer_flag)
                
                for ask_dict in chat_ask_dicts:
                    if ask_dict['seq'] in chatbot_log.keys():
                        continue
                    Flag = False
                    for answer_dict in chat_answer_dicts:
                        
                        if ask_dict['seq'] == answer_dict['seq']:
                            chatbot_log[answer_dict['seq']] = (answer_dict['ask'],answer_dict['answer'])
                            add_chatbot_log(answer_dict['seq'],answer_dict['ask'],answer_dict['answer'])
                            Flag = True
                            break
                    if Flag:
                        continue
                    else:
                        print ('model(%s) deal %s : %s'%(chat_ai.model_name,ask_dict['seq'],ask_dict['ask']))
                        result_flag,text = chat_ai.get_response(ask_dict['ask'])
                        if not result_flag:
                            print ('get response failed!')
                            continue
                        push_chatbot_answer(r,env.redis_answer_flag,ask_dict['seq'],text,ask_dict['ask'])
                        chatbot_log[ask_dict['seq']] = (ask_dict['ask'],text)
                        add_chatbot_log(ask_dict['seq'],ask_dict['ask'],text)
                        
            
                if activate_step%20 == 0:
                    if (not tc.check_on_line()) or (not tc.check_ai_online()):
                        break
                    if not tc.check_activate():        
                        print ('deactivate')
                        time.sleep(1)
                        print ('wait for activate...')
                        break
                    
                    # chatbot special redis clean
                    check_clear_redis(r,env=env)
                
                if activate_step>10000000:
                    activate_step = 0    
        
        if (not tc.check_on_line()) or (not tc.check_ai_online()):
            print ('caht bot server offline!')
            time.sleep(1)
            break
    