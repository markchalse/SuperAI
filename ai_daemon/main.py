import subprocess  
import time  
import sys
import psutil
import json
import redis
import os
import tempfile 
from config import EnvConfig


def set_ai_super_online(redis_obj,r_key):
    try:
        redis_obj.set(r_key, '1')
    except Exception as e:
        print (e)

def check_pid(pid):
    #pid = 16000  
    try:
        # 使用psutil检查PID  
        process = psutil.Process(pid)  
        if process.is_running():  
            print(f"PID {pid} is still running.")  
            return True
        else:
            print(f"PID {pid} is not running.")  
            return False
    except Exception as e:
        print(e) 
        return False   
        #if 'not found' in str(e):
            #print ('haha')
            #bat_path= r'F:\workspace\majun\zhiyuanchuang_space\ai_code\superai\SuperAI\code\data_sensor\camera_sensor\script\camera_redis_show.bat'
            #os.system('start '+bat_path)

def clear_redis(redis_obj,redis_key):
    pid_count = redis_obj.llen(redis_key)
    if pid_count>5:
        try:
            for i in range(pid_count-5):
               redis_str=redis_obj.lindex(redis_key, 0)
               serv_name,serv_pid,serv_time = analyze_redis_data(redis_str)
               if check_pid(int(serv_pid)):
                   break
               else:
                   redis_obj.lpop(redis_key)
        except Exception as e:
            print (e)

def analyze_redis_data(data):
    try:
        data_dict = json.loads(data)
        return data_dict['server'],data_dict['pid'],data_dict['time']
    except Exception as e:
        print (e)
        return '','',''

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
    
    set_ai_super_online(r,env.ai_online_flag)
    
    step = 0
    while True:
        if r.get(env.ai_online_flag) == b'0':
            print('SuperAI daemon offline!')
            break
        
        step+=1
        exist_servers = []
        server_pid_infos = r.lrange(env.server_pid_key, 0, -1)
        for server_pid_info in server_pid_infos:
            serv_name,serv_pid,serv_time = analyze_redis_data(server_pid_info)
            if check_pid(int(serv_pid)):
                exist_servers.append(serv_name)
        print ('exist servers:')
        print (exist_servers)
        
        
        for sys_serv_name in env.server_bat.keys():
            if sys_serv_name not in exist_servers:
                print ('start %s ...'%sys_serv_name)
                os.system('start '+env.server_bat[sys_serv_name])
                if step == 1:
                    time.sleep(3)
             
        
        if step%3 == 0:
            clear_redis(r,env.server_pid_key)
            print('clear redis over!')
        
        if step>10000000:
            step = 2
        
        if r.get(env.ai_online_flag) == b'0':
            print('SuperAI daemon offline!')
            break
        
        
        if step == 1:
            time.sleep(60)
        else:
            time.sleep(20)
        
    # 使用 atexit 清理锁文件（可选）  
    import atexit  
    atexit.register(os.remove, lock_path)  