import cv2  
import pickle  
import redis  
import base64
import numpy as np
import json
from PIL import Image 
from io import BytesIO

# 初始化Redis连接  
r = redis.Redis(host='localhost', port=6379, db=0)  

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
  

def get_image_from_redis(key):  
    #base64
    #base64_str = r.rpop(key)
    camera_json_str = r.lindex(key, -1)
    json_dict = json.loads(camera_json_str)
    camera_dict = json_dict['device']
    print ('%s : %s'%(json_dict['my_id'],json_dict['time']))
    base64_str = camera_dict['data']
    person_dict = camera_dict['person']
    
    #print (person_dict)
    
    for name in person_dict.keys():
        print (name)
        print (person_dict[name]['box'])
    
    if base64_str is not None:
        #image_array = base642numpyarray(base64_str,camera_dict['height'],camera_dict['width'])
        image_array = base642jpg2numpyarray(base64_str)
        return image_array
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