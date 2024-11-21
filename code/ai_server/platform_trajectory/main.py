


import os
import redis
import time

from config import EnvConfig
from thread_controller import ThreadControler
from redis_tools import *

import cv2

from utils import *





if __name__ == "__main__":
    
    # 初始化Redis连接  
    r = redis.Redis(host='localhost', port=6379, db=0)  
    
    print ('servo motor drive platform trajectory server online!')
    time.sleep(0.3)
    env = EnvConfig()
    
    tc = ThreadControler()
    tc.init_thread()
    
    pid = os.getpid()
    print(f"当前进程的PID是: {pid}")   
    push_server_pid(r,'ai_server_pid','platform_traj',str(pid)) #20241107
    
    print ('wait for activate...')
    
    
    while True:
        if not tc.check_activate():
            time.sleep(3)
        else:
            activate_step = 0
            print ('servo motor drive platform trajectory server activate!')
            
            traj_pool = Trajectory()
            
            traj_id = r.get(env.trajectory_id_key).decode('utf-8')
            print ('start tracking: %s'%traj_id)
            
            while True:
                activate_step+=1 
                
                image,box,width,height = get_image_from_redis(r,env.smpdr_result_key)  
                if image is None: 
                    print("No image available from Redis.")  
                    continue
                if box!='[]':
                    box_array = str_array2np_array_float(box)
                    #print (box_array)
                    traj_pool.trajx.append((box_array[0]+box_array[2])/2.0)
                    traj_pool.trajy.append((box_array[1]+box_array[3])/2.0)
                
                traj_img = pil_draw_pic(int(width),int(height),traj_pool.trajx,traj_pool.trajy,1.0)
                    
                
                push_image_to_redis(r,env.smpdj_result_key,traj_img,traj_pool.trajx,traj_pool.trajy,traj_id,activate_step)

                
                if activate_step%10 == 0:
                    new_id = r.get(env.trajectory_id_key).decode('utf-8')
                    if new_id!=traj_id:
                        traj_id = new_id
                        traj_pool = Trajectory()
                        print ('start tracking: %s'%traj_id)
                
                if activate_step%20 == 0:
                    if (not tc.check_on_line()) or (not tc.check_ai_online()):
                        break
                    if not tc.check_activate():        
                        print ('deactivate')
                        time.sleep(1)
                        print ('wait for activate...')
                        break
                    
                
                if activate_step>10000000:
                    activate_step = 0    
        
        if (not tc.check_on_line()) or (not tc.check_ai_online()):
            print ('servo motor drive platform trajectory server offline!')
            time.sleep(1)
            break
    
