


import os
import redis
import time

from config import EnvConfig
from thread_controller import ThreadControler
from redis_tools import *
import cv2
#from utils import *

from utils import str_array2np_array_float,get_straight_trajectory_LIP,get_straight_goal,get_graphic_goal,closest_multiple_of_five


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
    
    
    pid = os.getpid()
    print(f"当前进程的PID是: {pid}")   
    push_server_pid(r,'ai_server_pid','score',str(pid))
    
    print ('wait for activate...')
    
    
    while True:
        if not tc.check_activate():
            time.sleep(3)
        else:
            activate_step = 0
            
            print ('score control server activate!')
            
            
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
                else:
                    print ('-------------------------------------')
                    print('Now step id change : %s'%now_step_id)
                
                if last_step_id == 'ai_begin_step' or last_step_id == '0':
                    print ('Init proj cfg first time! Last step id : %s'%last_step_id)
                    last_step_id = now_step_id
                    ai_score = proj_cfg
                    print(ai_score)
                    try:
                        r.set(env.trajectory_id_key,get_now_YMDhmsms()+'_'+now_step_id)
                        push_redis_project_scores(r,env.project_scores_key,ai_score)
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
                
                pic_file_path = os.path.join(traj_pic_dir,traj_id+'.jpg')
                print ('Save trajectory pic at :%s'%pic_file_path)
                cv2.imwrite(pic_file_path,img)

                x_f,x_b,y_f,y_b=get_straight_goal(x_list,y_list,straight_score)

                square_goal,triangular_goal = get_graphic_goal(scores)
                
                
                
                #if last_step_id == "1845989300348694530":
                if last_step_id == env.square_goal_step_id:
                    result_score = square_goal
                #elif last_step_id == "1845989300348694532":
                elif last_step_id == env.triangular_goal_step_id:
                    result_score = triangular_goal
                else:
                    result_score = triangular_goal
                
                if last_step_id != '0':
                    #print ('search :',last_step_id)
                    for task_i in range(len(ai_score['taskList'])):
                        for step_i in range(len(ai_score['taskList'][task_i]['stepList'])):                            
                            if ai_score['taskList'][task_i]['stepList'][step_i]['stepId'] == last_step_id:
                                #print ('find!!!!')
                                ai_score['taskList'][task_i]['stepList'][step_i]['ai_score'] = str(closest_multiple_of_five(float(result_score['score'])*100))
                                ai_score['taskList'][task_i]['stepList'][step_i]['ai_comment'] = result_score['comment']
                                ai_score['taskList'][task_i]['stepList'][step_i]['ai_state'] = '1'
                
                print (ai_score)
                push_redis_project_scores(r,env.project_scores_key,ai_score)
                
                
                print ('project over , goodbye !')
                
                
                
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
                    
                    
                
                if activate_step>10000000:
                    activate_step = 0    
        
        if (not tc.check_on_line()) or (not tc.check_ai_online()):
            print ('score control server offline!')
            time.sleep(1)
            break
    