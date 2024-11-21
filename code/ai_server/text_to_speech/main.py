
import redis
#import cv2
import time

from utils import *
from thread_controller import ThreadControler
from config import EnvConfig

from redis_tools import *

if __name__ == "__main__":
    # 初始化Redis连接  
    r = redis.Redis(host='localhost', port=6379, db=0)  
    
    print ('text to thound server online!')
    time.sleep(0.3)
    env = EnvConfig()
    tc = ThreadControler()
    tc.init_thread()
    
    pid = os.getpid()
    print(f"当前进程的PID是: {pid}")   
    push_server_pid(r,'ai_server_pid','tts',str(pid))
    
    print ('wait for activate...')
    
    while True:
        if not tc.check_activate():
            time.sleep(3)
        else:
            
            
            if env.tts_model == 'edge':
                tts_engine = EdgeTTS()
            elif env.tts_model == 'pytts':
                tts_engine = PyTTS()
            else:
                print ('wrong tts model in config!')
                time.sleep(2)
                continue
            
            activate_step = 0
            
            print ('thound to sound server activate!')
            
            while True:
                activate_step+=1 

                sound_files = sound_file_names(env.tts_workspace)
                text_dicts = get_tts_texts(r,env.redis_text_flag)
                for text_dict in text_dicts:
                    if text_dict['seq'] in sound_files:
                        continue
                    else:
                        print ('deal %s : %s'%(text_dict['seq'],text_dict['text']))
                        #sound_file_name = os.path.join(env.tts_workspace,text_dict['seq']+'.mp3')
                        sound_file_name = os.path.join(env.tts_workspace,text_dict['seq']+'.wav')
                        tts_engine.text2voice_file(text_dict['text'],sound_file_name)
                        push_tts_result(r,env.redis_sound_flag,text_dict['seq'],text_dict['text'],sound_file_name)
            
                if activate_step%20 == 0:
                    if (not tc.check_on_line()) or (not tc.check_ai_online()):
                        break
                    if not tc.check_activate():        
                        print ('deactivate')
                        time.sleep(1)
                        print ('wait for activate...')
                        break
                    
                    # tts special redis clean
                    check_clear_redis(r,MAX_LEN=env.REDIS_MAX_LEN,env=env)
                
                if activate_step>10000000:
                    activate_step = 0    
        
        if (not tc.check_on_line()) or (not tc.check_ai_online()):
            print ('text to sound server offline!')
            time.sleep(1)
            break