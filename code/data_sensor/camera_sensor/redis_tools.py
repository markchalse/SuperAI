import redis
import base64

def push_image_to_redis(redis_object,processed_image):  
    r = redis_object
    # 将图像序列化为字节流  
    #image_bytes = pickle.dumps(processed_image)  
    # 数组直接转字符串
    image_str = processed_image.tostring()
    
    # Encode array string to Base64
    base64_str = base64.b64encode(image_str).decode('utf-8')
    

    image_store = base64_str
      
    # 检查Redis中的记录数  
    image_list_key = 'camera_images'
    image_count = r.llen(image_list_key)  
      
    # 如果记录数超过10条，弹出前面的8条  
    if image_count > 10:  
        try:
            r.lpop(image_list_key)  # 弹出一条，重复8次或使用循环  
        except Exception as e:
            print (e)
        # 或者使用管道操作一次性弹出多条  
        # pipe = r.pipeline()  
        # for _ in range(8):  
        #     pipe.lpop(image_list_key)  
        # pipe.execute()  
      
    # 将新的图像推送到Redis  
    try:
        r.rpush(image_list_key, image_store)
    except Exception as e:
        print (e)