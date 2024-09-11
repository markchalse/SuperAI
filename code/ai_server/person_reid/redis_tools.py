import redis
import base64
import json
import numpy as np
import time
import datetime
from PIL import Image 
from io import BytesIO

from config import EnvConfig

def get_now_YMDhmsms():
    timestamp = time.time()
    dt_object = datetime.datetime.fromtimestamp(timestamp)  
    # 获取毫秒部分  
    milliseconds = int((timestamp - int(timestamp)) * 1000)  
    # 格式化日期和时间字符串，并手动添加毫秒  
    formatted_time = dt_object.strftime("%Y%m%d%H%M%S") + str(milliseconds).zfill(3)  
    #print(formatted_time)  # 输出形如：2023-07-19 15:30:45.123
    return formatted_time


def get_name_boxes_from_redis(redis_connect,key):
    camera_json_str = redis_connect.lindex(key, -1)
    json_dict = json.loads(camera_json_str)
    return json_dict['device']['person'],json_dict['time']

def base642numpyarray(base64_str,height,width):
    # Decode Base64 string to image data
    image_data = base64.b64decode(base64_str)
    # Convert image data to NumPy array
    image_array = np.frombuffer(image_data, dtype=np.uint8)
    # 将一维数组转换为正确的形状 (720, 1280, 3)
    image_array_reshaped = image_array.reshape((int(height), int(width), 3)) 
    return image_array_reshaped

def base642jpg2numpyarray(base64_str):
    # 将Base64字符串解码为二进制数据 
    jpg_data = base64.b64decode(base64_str) 
    # 使用BytesIO将二进制数据转换为Pillow图像  
    image = Image.open(BytesIO(jpg_data)) 
    np_image = np.array(image)  
    # OpenCV使用BGR，所以如果需要，这里将RGB转换为BGR  
    #np_image = np_image[:, :, ::-1]  
    return np_image

    
def get_image_from_redis(redis_connect,key):
    camera_json_str = redis_connect.lindex(key, -1)
    json_dict = json.loads(camera_json_str)
    camera_dict = json_dict['device']
    print ('%s : %s'%(json_dict['my_id'],json_dict['time']))
    base64_str = camera_dict['data']
    if base64_str is not None:
        #majun 2024.9.11
        #image_array = base642numpyarray(base64_str,camera_dict['height'],camera_dict['width'])
        image_array = base642jpg2numpyarray(base64_str)
        return image_array,json_dict['time']
    else:
        return None,None
    
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
    
def push_image_to_redis(redis_object,image_list_key,processed_image,result_dict,count):  
    env = EnvConfig()
    
    r = redis_object
    height = processed_image.shape[0]
    width = processed_image.shape[1]
    
    #majun 2024.9.11
    #base64_str = array2base64(processed_image)
    base64_str = array2jpg2base64(processed_image)
    
    
    person_dict = {}
    for person in result_dict.values():
        #if person['name']!=env.defeat_match_name:
            person_dict[person['name']] = {}
            #person_dict[person['name']]['box'] = person['face_index']
            person_dict[person['name']]['box'] = person['box']
            
    push_dict = {"device":{'type_id':'101',
                           'device_id':'51',
                           'num_id':'0',
                           'width':str(width),
                           'height':str(height),
                           'data':base64_str,
                           'person':person_dict},
                 'my_id':'101_51_0',
                 'time':get_now_YMDhmsms()
                 }
    #camer_name = 'front_single'
    
    image_store = json.dumps(push_dict)
    
    
    
    
    #image_list_key = 'camera_images'
    
    
    
    # 检查Redis中的记录数  
    #后期优化一个进程专门来删除
    if count%100==0:
        image_count = r.llen(image_list_key)     
        # 如果记录数超过10条，弹出前面的8条  
        if image_count > 10:  
            try:
                #r.lpop(image_list_key)  # 弹出一条
                r.ltrim(image_list_key, -10, -1)  # 只保留列表中最新的10个元素
                print ('clean person ReID redis memory ready!')
            except Exception as e:
                print (e)
    
    #    count = 0
    #else:
    #    count+=1

      
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