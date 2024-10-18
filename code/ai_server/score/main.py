


import os
import redis
import time

from config import EnvConfig
from thread_controller import ThreadControler
from redis_tools import *
import cv2
#from utils import *

from utils import str_array2np_array_float,get_straight_trajectory_LIP,get_straight_goal,get_graphic_goal


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
            
            #proj_cfg = get_redis_project_cfg(r,env.project_cfg_key)
            #if len(proj_cfg) == 0:
            #    print ('project config is empty!')
            #    time.sleep(1)
            #    break
            last_step_id='ai_begin_step'
            
            traj_score_tool = ScoreEval()
            
            ai_score = {}
            
            while True:
                activate_step+=1 
                
                cfg_flag,proj_cfg,now_step_id = get_redis_project_cfg(r,env.project_cfg_key)
                if not cfg_flag:
                    print ('project config is wrong!')
                    time.sleep(1)
                    break
                
                
                if now_step_id == last_step_id:
                    if activate_step%20 == 0:
                        if (not tc.check_on_line()) or (not tc.check_ai_online()):
                            print ('offline in activate!')
                            break
                        if not tc.check_activate():        
                            print ('deactivate')
                            time.sleep(1)
                            print ('wait for activate...')
                            break
                    continue
                
                if last_step_id == 'ai_begin_step':
                    last_step_id = now_step_id
                    ai_score = proj_cfg
                    try:
                        r.set(env.trajectory_id_key,get_now_YMDhmsms()+'_'+now_step_id)
                    except Exception as e:
                        last_step_id = 'ai_begin_step'
                        print (e)
                    
                    continue
                
                
                
                img,traj_id,x_str,y_str = get_traj_result(r,env.platform_traj_result_key)
                print ('traj_id:',traj_id)
                if x_str!='[]':
                    x_list = str_array2np_array_float(x_str)
                    y_list = str_array2np_array_float(y_str)
                    traj_points = []
                    for i in range(len(x_list)):
                        traj_points.append([x_list[i],y_list[i]])
                    straight_score = get_straight_trajectory_LIP(traj_points)
                else:
                    x_list = []
                    y_list = []
                    straight_score = 0
                
                scores,item = traj_score_tool.get_score_from_image(img)

                print ('straight score:%f'%straight_score)
                print("Predicted shape:", item)
                print("result scores:",scores)
                cv2.imwrite(os.path.join(traj_pic_dir,traj_id+'.jpg'),img)

                x_f,x_b,y_f,y_b=get_straight_goal(x_list,y_list,straight_score)

                square_goal,triangular_goal = get_graphic_goal(scores)
                
                
            
                
                '''
                result_dict = {}
                result_dict['traj_id'] = traj_id
                if 'xf' in traj_id:
                    result_dict['x_forward'] = x_f
                elif 'xb' in traj_id:
                    result_dict['x_back'] = x_b
                elif 'yf' in traj_id:
                    result_dict['y_forward'] = y_f
                elif 'yb' in traj_id:
                    result_dict['y_back'] = y_b
                elif 'square' in traj_id:
                    result_dict['square'] = square_goal
                elif 'triangular' in traj_id:
                    result_dict['triangular'] = triangular_goal
                else:
                    result_dict['x_forward'] = x_f
                    result_dict['x_back'] = x_b
                    result_dict['y_forward'] = y_f
                    result_dict['y_back'] = y_b
                    
                    
                    result_dict['square'] = square_goal
                    result_dict['triangular'] = triangular_goal
                
                result_dict['straight'] = ['直线相似度：%s'%str(straight_score)]
                
                #result_dict['scores'] = [round(i, 4) for i in scores]
                #result_dict['comments'] = ['利用PLC指令实现了给定的%s轨迹，做的很好请继续保持！'%item]
                
                push_redis_project_scores(r,env.project_scores_key,result_dict)
                '''
                
                if last_step_id == "1845989300348694530":
                    result_score = square_goal
                elif last_step_id == "1845989300348694532":
                    result_score = triangular_goal
                else:
                    result_score = triangular_goal
                
                for task_i in range(len(ai_score['taskList'])):
                    if ai_score['taskList'][task_i]['stepList'][0]['stepId'] == last_step_id:
                        ai_score['taskList'][task_i]['stepList'][0]['ai_score'] = str(float(result_score['score'])*100)
                        ai_score['taskList'][task_i]['stepList'][0]['ai_comment'] = result_score['comment']
                        ai_score['taskList'][task_i]['stepList'][0]['ai_state'] = '1'
                        
                push_redis_project_scores(r,env.project_scores_key,ai_score)
                
                
                print ('project over , goodbye !')
                
                #r.set(env.server_activate_flag,'0')
                #time.sleep(1)
                
                #2024.10.17 majun
                last_step_id = now_step_id
                
                try:
                    r.set(env.trajectory_id_key,get_now_YMDhmsms()+'_'+now_step_id)
                except Exception as e:
                    last_step_id = 'ai_begin_step'
                    print (e)
                
                
            
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
                    # no need to clean
                    #check_clear_redis(r,env=env)
                
                if activate_step>10000000:
                    activate_step = 0    
        
        if (not tc.check_on_line()) or (not tc.check_ai_online()):
            print ('score control server offline!')
            time.sleep(1)
            break
    