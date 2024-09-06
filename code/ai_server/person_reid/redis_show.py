import cv2  
import pickle  
import redis  
import base64
import numpy as np
import json

# 初始化Redis连接  
r = redis.Redis(host='localhost', port=6379, db=0)  
  
def get_image_from_redis(key):  
    #base64
    #base64_str = r.rpop(key)
    camera_json_str = r.lindex(key, -1)
    json_dict = json.loads(camera_json_str)
    camera_dict = json_dict['device']
    print ('%s : %s'%(json_dict['type_id'],json_dict['time']))
    base64_str = camera_dict['data']
    person_dict = camera_dict['person']
    
    #print (person_dict)
    
    for name in person_dict.keys():
        print (name)
        print (person_dict[name]['box'])
    
    if base64_str is not None:
        #print (base64_str)
        
        # Decode Base64 string to image data
        image_data = base64.b64decode(base64_str)
        #print (image_data)
        
        # Convert image data to NumPy array
        image_array = np.frombuffer(image_data, dtype=np.uint8)
        #print(image_array)
        #print(image_array.shape)
        # 将一维数组转换为正确的形状 (480, 640, 3)
        #image_array_reshaped = image_array.reshape((480, 640, 3))
        image_array_reshaped = image_array.reshape((int(camera_dict['height']), int(camera_dict['width']), 3))
        

        #print (image_array_reshaped.shape)
        return image_array_reshaped
        #print(processed_image)
    else:
        return None 
      
    
      

r.set('ai_person_reid_show_down','0')    
  
# 主循环，持续从Redis读取并显示图像，直到用户按下'q'键  
#image_key = 'ai_face_recognition_images'  
image_key = '101_51_0'  
while True:  
    image = get_image_from_redis(image_key)  
    if image is None:  
        print("No image available from Redis.")  
        continue  
      
    cv2.imshow('Image from Redis', image)  
      
    # 等待按键，如果按下'q'则退出循环  
    if cv2.waitKey(1) & 0xFF == ord('q'):  
        break  
    
    if r.get('ai_person_reid_show_down')==b'1':
        break
  
# 销毁所有OpenCV窗口  
cv2.destroyAllWindows()