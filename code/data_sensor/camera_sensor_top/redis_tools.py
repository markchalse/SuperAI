import redis
import base64
import json

import time
import datetime
import numpy as np
from PIL import Image 
from io import BytesIO

def get_now_YMDhmsms():
    timestamp = time.time()
    dt_object = datetime.datetime.fromtimestamp(timestamp)  
    # 获取毫秒部分  
    milliseconds = int((timestamp - int(timestamp)) * 1000)  
    # 格式化日期和时间字符串，并手动添加毫秒  
    formatted_time = dt_object.strftime("%Y%m%d%H%M%S") + str(milliseconds).zfill(3)  
    #print(formatted_time)  # 输出形如：2023-07-19 15:30:45.123
    return formatted_time

def numpy_to_base64(numpy_array, quality=95):  
    #- quality: JPEG图像的质量，范围从1（最差）到95（最好）。 
    # 将NumPy数组转换为PIL图像  
    image = Image.fromarray(numpy_array.astype('uint8'))  # 确保数据类型为uint8  
    # 转换为JPEG格式  
    buffered = BytesIO()  
    image.save(buffered, format="JPEG", quality=quality)  
    
     # 将图像内容从BytesIO对象中获取，并编码为Base64  
    image_bytes = buffered.getvalue()  
    base64_str = base64.b64encode(image_bytes).decode('utf-8')  
      
    return base64_str
  
def array2base64(numpy_array):
    # 数组直接转字符串
    image_str = numpy_array.tostring()
    # Encode array string to Base64
    base64_str = base64.b64encode(image_str).decode('utf-8')  
    return base64_str  

def array2jpg2base64(numpy_array,quality=90):
    # 将NumPy数组转换为PIL图像  
    image = Image.fromarray(numpy_array.astype('uint8'))  # 确保数据类型为uint8  
    # 转换为JPEG格式  
    buffered = BytesIO()  
    image.save(buffered, format="JPEG", quality=quality)  
    # 将图像内容从BytesIO对象中获取，并编码为Base64  
    image_bytes = buffered.getvalue()  
    base64_str = base64.b64encode(image_bytes).decode('utf-8')  
    return base64_str
  

def push_image_to_redis(redis_object,processed_image,activate_step):  
    r = redis_object
    
    #print (processed_image.shape[0])
    height = processed_image.shape[0]
    width = processed_image.shape[1]
    
    #majun 2024.9.11
    #base64_str = array2base64(processed_image)
    base64_str = array2jpg2base64(processed_image)
    
    
    push_dict = {"device":{'type_id':'101',
                           'device_id':'1',
                           'num_id':'1',
                           'my_id':'101_1_1',
                           'width':str(width),
                           'height':str(height),
                           'data':base64_str},
                 "my_id":'101_1_1',
                 'time':get_now_YMDhmsms()
                 }
    #camer_name = 'front_single'
    
    image_store = json.dumps(push_dict)
    
    
    
    
    #image_list_key = 'camera_images'
    image_list_key = '101_1_1'
    
    
    
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
    
def push_server_pid(redis_object,pid_redis_key,server_name,pid):
    data = {'server':server_name,
            'pid':str(pid),
            'time':get_now_YMDhmsms()}
    try:
        redis_object.rpush(pid_redis_key, json.dumps(data))
    except Exception as e:
        print (e)