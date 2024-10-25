import redis
import json
import time
import datetime
import psutil
import os

def analyze_redis_data(data):
    try:
        data_dict = json.loads(data)
        return data_dict['server'],data_dict['pid'],data_dict['time']
    except Exception as e:
        print (e)
        return '','',''
    
def check_pid(pid_int):
    #pid = 16000  
    try:
        # 使用psutil检查PID  
        process = psutil.Process(pid_int)  
        if process.is_running():  
            print(f"PID {pid_int} is still running.")  
            return True
        else:
            print(f"PID {pid_int} is not running.")  
            return False
    except Exception as e:
        print(e) 
        return False

def clear_redis(redis_obj,redis_key):
    pid_count = redis_obj.llen(redis_key)
    if pid_count>10:
        try:
            for i in range(pid_count-10):
               redis_str=redis_obj.lindex(redis_key, 0)
               serv_name,serv_pid,serv_time = analyze_redis_data(redis_str)
               if check_pid(int(serv_pid)):
                   break
               else:
                   redis_obj.lpop(redis_key)
        except Exception as e:
            print (e)
    
def kill_pid(pid_str):
    try:
        os.system('taskkill /f /pid %s' % pid_str)
        return True
    except Exception as e:
        print (e)
        return False
    
def get_now_YMDhmsms():
    timestamp = time.time()
    dt_object = datetime.datetime.fromtimestamp(timestamp)  
    # 获取毫秒部分  
    milliseconds = int((timestamp - int(timestamp)) * 1000)  
    # 格式化日期和时间字符串，并手动添加毫秒  
    formatted_time = dt_object.strftime("%Y%m%d%H%M%S") + str(milliseconds).zfill(3)  
    #print(formatted_time)  # 输出形如：2023-07-19 15:30:45.123
    return formatted_time


#def set_ai_super_online(redis_obj,r_key):
#    try:
#        redis_obj.set(r_key, '1')
#    except Exception as e:
#        print (e)

def set_redis_key_up(redis_obj,redis_key):
    try:
        for _ in range(3):
            redis_obj.set(redis_key, '1')
            time.sleep(0.3)
    except Exception as e:
        print (e)
        
def set_redis_key_down(redis_obj,redis_key):
    try:
        for _ in range(3):
            redis_obj.set(redis_key, '0')
            time.sleep(0.3)
    except Exception as e:
        print (e)

def check_redis_key_up(redis_obj,redis_key):
    try:
        if redis_obj.get(redis_key) == b'1':
            return True
        else:
            return False
    except Exception as e:
        print (e)
        return False

def clear_old_data(redis_obj,server_pid_key):
    print('start clear old data!')
    nowtime_str = get_now_YMDhmsms()
    server_pid_infos = redis_obj.lrange(server_pid_key, 0, -1)
    for server_pid_info in server_pid_infos:
        serv_name,serv_pid,serv_time = analyze_redis_data(server_pid_info)
        if serv_time[0:8]!=nowtime_str[0:8]:
            print ('clear %s %s %s'%(serv_time,serv_name,serv_pid))
            try:
                redis_obj.lpop(server_pid_key)
            except Exception as e:
                print(e)
                return False
                #break
        else:
            break
    return True  

def kill_exist_thread(redis_obj,server_pid_key):
    print('kill exist thread!')
    server_pid_infos = redis_obj.lrange(server_pid_key, 0, -1)
    for server_pid_info in server_pid_infos:
        serv_name,serv_pid,serv_time = analyze_redis_data(server_pid_info)
        if check_pid(int(serv_pid)):
            for _ in range(5):
                print ('kill server : %s'%serv_name)
                flag = kill_pid(serv_pid)
                time.sleep((_+1)*2)
                if flag:
                    break
            if not flag:
                return False
    return True