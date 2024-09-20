import redis


import json
import time
import datetime

from config import EnvConfig

#from utils import sound_file_names


def get_redis_project_cfg(redis_object,redis_key):
    try:
        # 假设redis_key是'project_cfg'，返回的是json格式的字符串  
        project_cfg = redis_object.get(redis_key).decode('utf-8')
        return json.loads(project_cfg)
        #return {'params':[0.9,0.8,0.7],'mission':['mission1','mission2','mission3']}
    except Exception as e:
        print (e)
        return {}

def push_redis_project_scores(redis_object,redis_key,score_result:dict):
    
    #推送到Redis  
    try:
        redis_object.rpush(redis_key, json.dumps(score_result))
    except Exception as e:
        print (e)

def get_now_YMDhmsms():
    timestamp = time.time()
    dt_object = datetime.datetime.fromtimestamp(timestamp)  
    # 获取毫秒部分  
    milliseconds = int((timestamp - int(timestamp)) * 1000)  
    # 格式化日期和时间字符串，并手动添加毫秒  
    formatted_time = dt_object.strftime("%Y%m%d%H%M%S") + str(milliseconds).zfill(3)  
    #print(formatted_time)  # 输出形如：2023-07-19 15:30:45.123
    return formatted_time


def set_chatbot_ask(redis_object,redis_key,ask):
    time_str = get_now_YMDhmsms()
    push_dict = {
        'seq':time_str,
        'ask':ask,
        'time':time_str
    }
    #推送到Redis  
    try:
        redis_object.rpush(redis_key, json.dumps(push_dict))
    except Exception as e:
        print (e)
        

def get_redis_chatbot(redis_object,redis_key):
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

def push_chatbot_answer(redis_object,redis_key,seq,answer,ask):
    push_dict = {
        'seq':seq,
        'ask':ask,
        'time':get_now_YMDhmsms(),
        'answer':answer
    }
    #推送到Redis  
    try:
        redis_object.rpush(redis_key, json.dumps(push_dict))
    except Exception as e:
        print (e)

'''
def check_clear_redis(redis_obj,env = EnvConfig()):
    from utils import read_chatbot_log
    chatbot_log = read_chatbot_log()
    chat_ask_count = redis_obj.llen(env.redis_ask_flag)
    if chat_ask_count>env.MAX_LEN:
        try:
            for i in range(chat_ask_count-env.MAX_LEN):
                redis_str = redis_obj.lindex(env.redis_ask_flag, 0)
                json_dict = json.loads(redis_str)
                if json_dict['seq'] in chatbot_log.keys():
                    redis_obj.lpop(env.redis_ask_flag)
                else:
                    break
            print ('clean chatbot ask redis memory ready!')
            
        except Exception as e:
            print (e)
            
    if redis_obj.llen(env.redis_answer_flag)>env.MAX_LEN:
        try:
            redis_obj.ltrim(env.redis_answer_flag, -env.MAX_LEN, -1)  # 只保留列表中最新的10个元素
            print ('clean chatbot answer redis memory ready!')
        except Exception as e:
            print (e)
'''    
        
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
 
if __name__ == "__main__":
    r = redis.Redis(host='localhost', port=6379, db=0)
    set_chatbot_ask(r,'ai_chatbot_ask',r'介绍一下你自己')