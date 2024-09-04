import redis


import json
import time
import datetime

from config import EnvConfig

from utils import sound_file_names


def get_now_YMDhmsms():
    timestamp = time.time()
    dt_object = datetime.datetime.fromtimestamp(timestamp)  
    # 获取毫秒部分  
    milliseconds = int((timestamp - int(timestamp)) * 1000)  
    # 格式化日期和时间字符串，并手动添加毫秒  
    formatted_time = dt_object.strftime("%Y%m%d%H%M%S") + str(milliseconds).zfill(3)  
    #print(formatted_time)  # 输出形如：2023-07-19 15:30:45.123
    return formatted_time


def set_tts_text(redis_object,redis_key,text):
    time_str = get_now_YMDhmsms()
    push_dict = {
        'seq':time_str,
        'text':text,
        'time':time_str
    }
    #推送到Redis  
    try:
        redis_object.rpush(redis_key, json.dumps(push_dict))
    except Exception as e:
        print (e)
        

def get_tts_texts(redis_object,redis_key):
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

def push_tts_result(redis_object,redis_key,seq,text,file_path):
    push_dict = {
        'seq':seq,
        'text':text,
        'time':get_now_YMDhmsms(),
        'path':file_path
    }
    #推送到Redis  
    try:
        redis_object.rpush(redis_key, json.dumps(push_dict))
    except Exception as e:
        print (e)


def check_clear_redis(redis_obj,MAX_LEN = 3,env = EnvConfig()):
    sound_files = sound_file_names(env.tts_workspace)
    tts_text_count = redis_obj.llen(env.redis_text_flag)
    if tts_text_count>MAX_LEN:
        try:
            for i in range(tts_text_count-MAX_LEN):
                redis_str = redis_obj.lindex(env.redis_text_flag, 0)
                json_dict = json.loads(redis_str)
                if json_dict['seq'] in sound_files:
                    redis_obj.lpop(env.redis_text_flag)
                else:
                    break
            print ('clean tts text redis memory ready!')
            
        except Exception as e:
            print (e)
            
    if redis_obj.llen(env.redis_sound_flag)>MAX_LEN:
        try:
            redis_obj.ltrim(env.redis_sound_flag, -MAX_LEN, -1)  # 只保留列表中最新的10个元素
            print ('clean tts sound redis memory ready!')
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
 
if __name__ == "__main__":
    r = redis.Redis(host='localhost', port=6379, db=0)  
    #set_tts_text(r,'ai_tts_text','你好，我想听一下你的声音')
    #set_tts_text(r,'ai_tts_text','豫章故郡，洪都新府。星分翼轸，地接衡庐。襟三江而带五湖，控蛮荆而引瓯越。物华天宝，龙光射牛斗之墟；人杰地灵，徐孺下陈蕃之榻。雄州雾列，俊采星驰。台隍枕夷夏之交，宾主尽东南之美。都督阎公之雅望，棨戟遥临')
    #set_tts_text(r,'ai_tts_text','宇文新州之懿范，襜帷暂驻。十旬休假，胜友如云。千里逢迎，高朋满座。腾蛟起凤，孟学士之词宗。紫电青霜，王将军之武库。家君作宰，路出名区；童子何知，躬逢胜饯。')
    #set_tts_text(r,'ai_tts_text','祝你生日快乐！')
    set_tts_text(r,'ai_tts_text','以下为演示功能！')