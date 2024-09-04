from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

import os
import redis
import time


from config import EnvConfig
from thread_controller import ThreadControler
from utils import *
from redis_tools import *

class AutomaticSpeechRecognition:
    def __init__(self):
        self.env = EnvConfig()
        self.asr_model = pipeline(task=Tasks.auto_speech_recognition,
                                  model=self.env.ASR_MODEL_PATH)
    
    def recognition(self,wav_path):
        if os.path.exists(wav_path):
             result = self.asr_model(wav_path)
             return result['text']
        else:
            print ("no wav file exists!")
            return ""


if __name__ == "__main__":
    asr_engine = AutomaticSpeechRecognition()
    asr_log = read_asr_log()
    # 初始化Redis连接  
    r = redis.Redis(host='localhost', port=6379, db=0)  
    
    print ('voice to word server online!')
    time.sleep(0.3)
    env = EnvConfig()
    tc = ThreadControler()
    tc.init_thread()
    print ('wait for activate...')
    
    
    #print (asr_engine.recognition(r'F:\workspace\majun\img\asr_example.wav'))
    
    
    while True:
        if not tc.check_activate():
            time.sleep(3)
        else:
            activate_step = 0
            
            print ('voice to word server activate!')
            
            while True:
                activate_step+=1 
                
                asr_voice_dicts = get_redis_asr(r,env.redis_sound_flag)
                asr_text_dicts = get_redis_asr(r,env.redis_text_flag)
                
                for voice_dict in asr_voice_dicts:
                    if voice_dict['seq'] in asr_log.keys():
                        continue
                    Flag = False
                    for asr_text_dict in asr_text_dicts:
                        
                        if voice_dict['seq'] == asr_text_dict['seq']:
                            asr_log[asr_text_dict['seq']] = (asr_text_dict['path'],asr_text_dict['text'])
                            add_asr_log(asr_text_dict['seq'],asr_text_dict['path'],asr_text_dict['text'])
                            Flag = True
                            break
                    if Flag:
                        continue
                    else:
                        print ('deal %s : %s'%(voice_dict['seq'],voice_dict['path']))
                        try:
                            text = asr_engine.recognition(voice_dict['path'])
                            print (text)
                        except Exception as e:
                            print (e)
                        push_asr_result(r,env.redis_text_flag,voice_dict['seq'],text,voice_dict['path'])
                        asr_log[voice_dict['seq']] = (voice_dict['path'],text)
                        add_asr_log(voice_dict['seq'],voice_dict['path'],text)
                        
            
                if activate_step%20 == 0:
                    if not tc.check_on_line():
                        break
                    if not tc.check_activate():        
                        print ('deactivate')
                        time.sleep(1)
                        print ('wait for activate...')
                        break
                    
                    # asr special redis clean
                    check_clear_redis(r,env=env)
                
                if activate_step>10000000:
                    activate_step = 0    
        
        if not tc.check_on_line():
            print ('voice to word server offline!')
            time.sleep(1)
            break
    