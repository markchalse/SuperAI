import redis
import base64
import json

import time
import datetime
import numpy as np

def get_now_YMDhmsms():
    timestamp = time.time()
    dt_object = datetime.datetime.fromtimestamp(timestamp)  
    # 获取毫秒部分  
    milliseconds = int((timestamp - int(timestamp)) * 1000)  
    # 格式化日期和时间字符串，并手动添加毫秒  
    formatted_time = dt_object.strftime("%Y%m%d%H%M%S") + str(milliseconds).zfill(3)  
    #print(formatted_time)  # 输出形如：2023-07-19 15:30:45.123
    return formatted_time

def push_image_to_redis(redis_object,processed_image,activate_step):  
    r = redis_object
    
    #print (processed_image.shape[0])
    height = processed_image.shape[0]
    width = processed_image.shape[1]
    
    ##########################################################################
    # 将图像序列化为字节流  
    #image_bytes = pickle.dumps(processed_image)  
    # 数组直接转字符串
    #image_str = np.array2string(processed_image.flatten())
    #processed_image = processed_image.flatten()
    #print (processed_image.shape)
    #image_str = str(processed_image)
    #print (len(image_str))
    #print (image_str)
    
    #new_array = eval(image_str)
    #print(new_array.shape)
    ##########################################################################
    image_str = processed_image.tostring()
    #print (image_str)
    
    # Encode array string to Base64
    base64_str = base64.b64encode(image_str).decode('utf-8')
    
    
    push_dict = {"device":{'type_id':'101',
                           'device_id':'1',
                           'num_id':'0',
                           'my_id':'101_1_0',
                           'width':str(width),
                           'height':str(height),
                           'time':get_now_YMDhmsms(),
                           'data':base64_str}}
                           #'data':image_str}}
    #camer_name = 'front_single'
    
    image_store = json.dumps(push_dict)
    
    
    
    
    #image_list_key = 'camera_images'
    image_list_key = '101_1_0'
    
    
    
    # 检查Redis中的记录数  
    #后期优化一个进程专门来删除
    if activate_step%100==0:
        image_count = r.llen(image_list_key)     
        # 如果记录数超过10条，弹出前面的8条  
        if image_count > 10:  
            try:
                #r.lpop(image_list_key)  # 弹出一条
                r.ltrim(image_list_key, -10, -1)  # 只保留列表中最新的10个元素
                print ('clean singal camera redis memory ready!')
            except Exception as e:
                print (e)
      
    # 将新的图像推送到Redis  
    try:
        r.rpush(image_list_key, image_store)
    except Exception as e:
        print (e)
    
    #return count