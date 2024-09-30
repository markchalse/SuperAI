


import os
import redis
import time

from config import EnvConfig
from thread_controller import ThreadControler
from redis_tools import *
import cv2
#from utils import *

from utils import str_array2np_array_float,get_straight_trajectory_LIP


from tools.traj_score_train.model.eval_one import ScoreEval




if __name__ == "__main__":
    #asr_engine = AutomaticSpeechRecognition()
    #chatbot_log = read_chatbot_log()
    
    
    # 初始化Redis连接  
    r = redis.Redis(host='localhost', port=6379, db=0)  
    
    print ('score control server online!')
    time.sleep(0.3)
    env = EnvConfig()
    
    
    ###dir
    traj_pic_dir = os.path.join(env.score_space,'trajectory')
    if not os.path.exists(traj_pic_dir):
        os.mkdir(traj_pic_dir)
    
    ###
    
    
    tc = ThreadControler()
    tc.init_thread()
    print ('wait for activate...')
    
    
    while True:
        if not tc.check_activate():
            time.sleep(3)
        else:
            activate_step = 0
            
            print ('score control server activate!')
            
            proj_cfg = get_redis_project_cfg(r,env.project_cfg_key)
            if len(proj_cfg) == 0:
                print ('project config is empty!')
                time.sleep(1)
                break
            
            traj_score_tool = ScoreEval()
            
            while True:
                activate_step+=1 
                
                #chat_ask_dicts = get_redis_chatbot(r,env.redis_ask_flag)
                #chat_answer_dicts = get_redis_chatbot(r,env.redis_answer_flag)
                
                
                '''
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
                '''
                
                
                #push_redis_project_scores(r,env.project_scores_key,{'project1':{'scores':[5,3,4],'comment':['best','good','bad']}})
                #from utils import jungement
                #push_redis_project_scores(r,env.project_scores_key,jungement(len(proj_cfg['mission'])))
                
                img,traj_id,x_str,y_str = get_traj_result(r,env.platform_traj_result_key)
                print (traj_id)
                if x_str!='[]':
                    x_list = str_array2np_array_float(x_str)
                    y_list = str_array2np_array_float(y_str)
                    traj_points = []
                    for i in range(len(x_list)):
                        traj_points.append([x_list[i],y_list[i]])
                    straight_score = get_straight_trajectory_LIP(traj_points)
                else:
                    straight_score = 0
                
                scores,item = traj_score_tool.get_score_from_image(img)

                print ('straight score:%f'%straight_score)
                print("Predicted shape:", item)
                print("result scores:",scores)
                cv2.imwrite(os.path.join(traj_pic_dir,traj_id+'.jpg'),img)

                result_dict = {}
                result_dict['straight'] = ['直线相似度：%s'%str(straight_score)]
                result_dict['scores'] = [round(i, 4) for i in scores]
                result_dict['comments'] = ['利用PLC指令实现了给定的%s轨迹，做的很好请继续保持！'%item]
                push_redis_project_scores(r,env.project_scores_key,result_dict)
                
                
                print ('class over , goodbye !')
                
                r.set(env.server_activate_flag,'0')
                time.sleep(1)
                break
            
                if activate_step%20 == 0:
                    if (not tc.check_on_line()) or (not tc.check_ai_online()):
                        print ('offline in activate!')
                        break
                    if not tc.check_activate():        
                        print ('deactivate')
                        time.sleep(1)
                        print ('wait for activate...')
                        break
                    
                    # score control special redis clean
                    #check_clear_redis(r,env=env)
                
                if activate_step>10000000:
                    activate_step = 0    
        
        if (not tc.check_on_line()) or (not tc.check_ai_online()):
            print ('score control server offline!')
            time.sleep(1)
            break
    