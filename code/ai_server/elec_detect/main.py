


import os
import redis
import time

from config import EnvConfig
from thread_controller import ThreadControler
from redis_tools import *
from utils import *





if __name__ == "__main__":
    #asr_engine = AutomaticSpeechRecognition()
    chatbot_log = read_chatbot_log()
    # 初始化Redis连接  
    r = redis.Redis(host='localhost', port=6379, db=0)  
    
    print ('chat bot server online!')
    time.sleep(0.3)
    env = EnvConfig()
    if env.chat_model_name == "GLM":
        chat_ai = GLM()
    else:
        chat_ai = BaiduAI()
    tc = ThreadControler()
    tc.init_thread()
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
                        print ('deal %s : %s'%(ask_dict['seq'],ask_dict['ask']))
                        try:
                            text = chat_ai.get_response(ask_dict['ask'])
                            #print (text)
                        except Exception as e:
                            print (e)
                        push_chatbot_answer(r,env.redis_answer_flag,ask_dict['seq'],text,ask_dict['ask'])
                        chatbot_log[ask_dict['seq']] = (ask_dict['ask'],text)
                        add_chatbot_log(ask_dict['seq'],ask_dict['ask'],text)
                        
            
                if activate_step%20 == 0:
                    if not tc.check_on_line():
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
        
        if not tc.check_on_line():
            print ('caht bot server offline!')
            time.sleep(1)
            break
    