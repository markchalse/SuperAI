
import redis
import cv2

from redis_tools import get_image_from_redis,push_image_to_redis
from login import LogIn

# 初始化Redis连接  
r = redis.Redis(host='localhost', port=6379, db=0)  

#image_key = 'camera_images'
image_key = '101_1_0'



if __name__ == "__main__":
    log_tool = LogIn()
    r.set('face_recognition_down','0')
    # 主循环，持续从Redis读取并显示图像，直到用户按下'q'键 
    push_count = 0
    while True:
        image = get_image_from_redis(r,image_key)  
        if image is None:  
            print("No image available from Redis.")  
            continue  
        
        result_img,result_names = log_tool.process(image)
        #push_count = push_image_to_redis(r,'face_recognition_images',result_img,push_count)
        push_count = push_image_to_redis(r,'101_50_0',result_img,push_count)
        
        
        
        print (result_names)
        #cv2.imshow('Login Image', result_img)
        # 等待按键，如果按下'q'则退出循环  
        #if cv2.waitKey(1) & 0xFF == ord('q'):  
        #    break  
        
        if push_count%30 == 0:
            if r.get('face_recognition_down')==b'1':
                break
    # 销毁所有OpenCV窗口  
    cv2.destroyAllWindows()