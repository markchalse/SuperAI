import redis
import base64
import json

import time
import datetime

def get_now_YMDhmsms():
    timestamp = time.time()
    dt_object = datetime.datetime.fromtimestamp(timestamp)  
    # 获取毫秒部分  
    milliseconds = int((timestamp - int(timestamp)) * 1000)  
    # 格式化日期和时间字符串，并手动添加毫秒  
    formatted_time = dt_object.strftime("%Y%m%d%H%M%S") + str(milliseconds).zfill(3)  
    #print(formatted_time)  # 输出形如：2023-07-19 15:30:45.123
    return formatted_time

def push_image_to_redis(redis_object,processed_image,count):  
    r = redis_object
    
    # 将图像序列化为字节流  
    #image_bytes = pickle.dumps(processed_image)  
    # 数组直接转字符串
    image_str = processed_image.tostring()
    # Encode array string to Base64
    base64_str = base64.b64encode(image_str).decode('utf-8')
    
    
    push_dict = {'camera_name':'front_single',
                 'width':'1920','height':1080,
                 'time':get_now_YMDhmsms(),
                 'data':base64_str}
    #camer_name = 'front_single'
    
    image_store = json.dumps(push_dict)
    
    
    
    
    image_list_key = 'camera_images'
    
    
    
    # 检查Redis中的记录数  
    #后期优化一个进程专门来删除
    if count>100:
        image_count = r.llen(image_list_key)     
        # 如果记录数超过10条，弹出前面的8条  
        if image_count > 10:  
            try:
                #r.lpop(image_list_key)  # 弹出一条
                r.ltrim(image_list_key, -10, -1)  # 只保留列表中最新的10个元素
            except Exception as e:
                print (e)
        count = 0
    else:
        count+=1

      
    # 将新的图像推送到Redis  
    try:
        r.rpush(image_list_key, image_store)
    except Exception as e:
        print (e)
    
    return count