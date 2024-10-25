


import os
import redis
import time

from config import EnvConfig
from thread_controller import ThreadControler
from redis_tools import *

import cv2

from utils import *





if __name__ == "__main__":
    #asr_engine = AutomaticSpeechRecognition()
    #chatbot_log = read_chatbot_log()
    
    # 初始化Redis连接  
    r = redis.Redis(host='localhost', port=6379, db=0)  
    
    print ('servo motor drive platform recognition server online!')
    time.sleep(0.3)
    env = EnvConfig()
    
    tc = ThreadControler()
    tc.init_thread()
    
    pid = os.getpid()
    print(f"当前进程的PID是: {pid}")   
    push_server_pid(r,'ai_server_pid','smdpr',str(pid))
    
    print ('wait for activate...')
    
    
    while True:
        if not tc.check_activate():
            time.sleep(3)
        else:
            activate_step = 0
            track_tool = StartTrack()
            print ('servo motor drive platform recognition server activate!')
            
            while True:
                activate_step+=1 
                
                image = get_image_from_redis(r,env.camera_source_key)  
                if image is None: 
                    print("No image available from Redis.")  
                    continue
                
                box = track_tool.get_tracker_results(image)
                if len(box) > 0:
                    #print(box)
                    cv2.rectangle(image,(int(box[0]),int(box[1])),(int(box[2]),int(box[3])),(255,0,0),25)
                push_image_to_redis(r,env.smpdr_result_key,image,box,activate_step)
                #cv2.imshow('smdpr Image', image)        
                #if cv2.waitKey(1) & 0xFF == ord('q'):  
                #    break  
                
                if activate_step%20 == 0:
                    if (not tc.check_on_line()) or (not tc.check_ai_online()):
                        break
                    if not tc.check_activate():        
                        print ('deactivate')
                        time.sleep(1)
                        print ('wait for activate...')
                        break
                    
                    # servo motor drive platform recognition clean
                    #check_clear_redis(r,env=env)
                
                if activate_step>10000000:
                    activate_step = 0    
        
        if (not tc.check_on_line()) or (not tc.check_ai_online()):
            print ('servo motor drive platform recognition server offline!')
            time.sleep(1)
            break
    #cv2.destroyAllWindows()