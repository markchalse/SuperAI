import subprocess  
import time  
import sys
import psutil
import json
import redis
import os
import tempfile 
from config import EnvConfig
from utils import *








if __name__== "__main__":
    env = EnvConfig()
    
    #------------------------lock--------------------------------
    # 自定义锁文件的路径和名字  
    lock_path = env.codebase_path+'/ai_daemon/tmp.lock'  
    
    # 尝试写入锁文件  
    try:  
        with open(lock_path, 'x') as f:  # 使用 'x' 模式来确保文件不存在时才创建  
            f.write('lock')  
        # 继续程序的其他部分  
        print("程序正常运行")  
    except FileExistsError:  
        print("程序已在运行，退出新实例")  
        # 如果需要，可以手动删除锁文件（但在这个例子中，我们可能不这样做）  
        # os.remove(lock_path)  
        exit(1)  
    #------------------------lock--------------------------------
    r = redis.Redis(host='localhost', port=6379, db=0)  
    
    set_redis_key_up(r,env.ai_online_flag)
    print ('Super AI on line')
    
    if not clear_old_data(r,env.server_pid_key):
        print ('clear old thread data fail!')
        exit(0)
    
    if not kill_exist_thread(r,env.server_pid_key):
        print ('kill exist thread fail!')
        exit(0)
    
    #close all
    print ('Begin init all server flag:')
    for server_name in env.server_pool:
        print (server_name)
        set_redis_key_down(r,env.server_code_info[server_name]['online_flag'])
        set_redis_key_down(r,env.server_code_info[server_name]['activate_flag'])
        time.sleep(0.2)

    step = 0
    while True:
        step+=1

        if r.get(env.ai_online_flag) == b'0':
            print('SuperAI daemon offline!')
            break
        

        
        exist_servers = []
        server_pid_infos = r.lrange(env.server_pid_key, 0, -1)
        for server_pid_info in server_pid_infos:
            serv_name,serv_pid,serv_time = analyze_redis_data(server_pid_info)
            if check_pid(int(serv_pid)):
                exist_servers.append(serv_name)
        print ('exist servers:')
        print (exist_servers)
        
        
        for sys_serv_name in env.server_pool:
            if sys_serv_name not in exist_servers:
                print ('start %s ...'%sys_serv_name)
                os.system('start '+env.server_code_info[sys_serv_name]['start'])
                time.sleep(2)
                print ('wait %s activate ...'%sys_serv_name)
                
                for _ in range(5):
                    if not check_redis_key_up(r,env.server_code_info[sys_serv_name]['activate_flag']):
                        print ('set activate ...')
                        set_redis_key_up(r,env.server_code_info[sys_serv_name]['activate_flag'])
                        time.sleep((_+1)*5)
                    else:
                        #break
                        print ('stil activate , wait ...')
                        #time.sleep((_+1)*3)
                        time.sleep(3)
                
                #if step == 1:
                #    time.sleep(3)
            else:
                print ('%s is still running'%sys_serv_name)
            
        
        
        if step%3 == 0:
            clear_redis(r,env.server_pid_key)
            print('clear PID redis over!')
        
        if step>10000000:
            step = 1
        
        if r.get(env.ai_online_flag) == b'0':
            print('SuperAI daemon offline!')
            time.sleep(0.1)
            break
        
        
        #if step == 1:
        #    time.sleep(60)
        #else:
        time.sleep(20)
        
    # 使用 atexit 清理锁文件（可选）  
    import atexit  
    atexit.register(os.remove, lock_path)  