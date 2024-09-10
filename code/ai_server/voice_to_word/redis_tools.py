import redis


import json
import time
import datetime

from config import EnvConfig

#from utils import sound_file_names


def get_now_YMDhmsms():
    timestamp = time.time()
    dt_object = datetime.datetime.fromtimestamp(timestamp)  
    # 获取毫秒部分  
    milliseconds = int((timestamp - int(timestamp)) * 1000)  
    # 格式化日期和时间字符串，并手动添加毫秒  
    formatted_time = dt_object.strftime("%Y%m%d%H%M%S") + str(milliseconds).zfill(3)  
    #print(formatted_time)  # 输出形如：2023-07-19 15:30:45.123
    return formatted_time


def set_asr_voice(redis_object,redis_key,path):
    time_str = get_now_YMDhmsms()
    push_dict = {
        'seq':time_str,
        'path':path,
        'time':time_str
    }
    #推送到Redis  
    try:
        redis_object.rpush(redis_key, json.dumps(push_dict))
    except Exception as e:
        print (e)
        

def get_redis_asr(redis_object,redis_key):
    list_values = redis_object.lrange(redis_key, 0, -1)
    result = []
    for value in list_values:  
        try:
            # 假设每个值都是JSON格式的字符串  
            dict_value = json.loads(value)  
            result.append(dict_value)  
        except json.JSONDecodeError:  
            # 如果转换失败（例如，字符串不是有效的JSON），可以打印错误或处理异常  
            print(f"无法将字符串 {value} 转换为字典")  
    return result

def push_asr_result(redis_object,redis_key,seq,text,file_path):
    push_dict = {
        'seq':seq,
        'path':file_path,
        'time':get_now_YMDhmsms(),
        'text':text
    }
    #推送到Redis  
    try:
        redis_object.rpush(redis_key, json.dumps(push_dict))
    except Exception as e:
        print (e)


def check_clear_redis(redis_obj,env = EnvConfig()):
    from utils import read_asr_log
    asr_log = read_asr_log()
    asr_sound_count = redis_obj.llen(env.redis_sound_flag)
    if asr_sound_count>env.MAX_LEN:
        try:
            for i in range(asr_sound_count-env.MAX_LEN):
                redis_str = redis_obj.lindex(env.redis_sound_flag, 0)
                json_dict = json.loads(redis_str)
                if json_dict['seq'] in asr_log.keys():
                    redis_obj.lpop(env.redis_sound_flag)
                else:
                    break
            print ('clean asr sound redis memory ready!')
            
        except Exception as e:
            print (e)
            
    if redis_obj.llen(env.redis_text_flag)>env.MAX_LEN:
        try:
            redis_obj.ltrim(env.redis_text_flag, -env.MAX_LEN, -1)  # 只保留列表中最新的10个元素
            print ('clean asr word redis memory ready!')
        except Exception as e:
            print (e)
    
        
'''
def redis_show(redis_key):
    env = EnvConfig()
    r = redis.Redis(host='localhost', port=6379, db=0)  
    if redis_key == 'tts_text':
        key = env.redis_text_flag  
    else:
        key = env.redis_sound_flag
    results = []
    list_values = r.lrange(key, 0, -1)
    for value in list_values:
        dict_value = json.loads(value)  
        results.append(dict_value)
    for result in results:
        print (result)
    return results
'''
def push_server_pid(redis_object,pid_redis_key,server_name,pid):
    data = {'server':server_name,
            'pid':str(pid),
            'time':get_now_YMDhmsms()}
    try:
        redis_object.rpush(pid_redis_key, json.dumps(data))
    except Exception as e:
        print (e)
         
if __name__ == "__main__":
    r = redis.Redis(host='localhost', port=6379, db=0)
    set_asr_voice(r,'ai_asr_sound',r'F:\workspace\majun\img\asr_example.wav')