import redis
import base64
import json

def push_image_to_redis(redis_object,processed_image):  
    r = redis_object
    
    # 将图像序列化为字节流  
    #image_bytes = pickle.dumps(processed_image)  
    # 数组直接转字符串
    image_str = processed_image.tostring()
    # Encode array string to Base64
    base64_str = base64.b64encode(image_str).decode('utf-8')
    
    
    push_dict = {'camera_name':'front_single',
                 'width':'1920','height':1080,
                 'time':'20230814104812003',
                 'data':base64_str}
    #camer_name = 'front_single'
    
    image_store = json.dumps(push_dict)
    
    
    
    
    image_list_key = 'camera_images'
    
    # 检查Redis中的记录数  
    #后期优化一个进程专门来删除
    image_count = r.llen(image_list_key)  
      
    # 如果记录数超过10条，弹出前面的8条  
    if image_count > 10:  
        try:
            r.lpop(image_list_key)  # 弹出一条
        except Exception as e:
            print (e)

      
    # 将新的图像推送到Redis  
    try:
        r.rpush(image_list_key, image_store)
    except Exception as e:
        print (e)