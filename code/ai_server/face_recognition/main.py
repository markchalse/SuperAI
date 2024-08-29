
import redis
import cv2
import time


from redis_tools import get_image_from_redis,push_image_to_redis
from login import LogIn

from thread_controller import ThreadControler

from config import EnvConfig

# 初始化Redis连接  
r = redis.Redis(host='localhost', port=6379, db=0)  

if __name__ == "__main__":
    print ('face recognition server online!')
    time.sleep(0.3)
    env = EnvConfig()
    tc = ThreadControler()
    tc.init_thread()
    print ('wait for activate...')
    
    while True:
        if not tc.check_activate():
            time.sleep(3)
        else:
            
    
            log_tool = LogIn()
            #r.set('face_recognition_down','0')
            # 主循环，持续从Redis读取并显示图像，直到用户按下'q'键 
            push_count = 0
            activate_step = 0
            while True:
                activate_step+=1 
                image = get_image_from_redis(r,env.camera_img_list_redis_key)  
                if image is None:  
                    print("No image available from Redis.")  
                    continue  
        
                result_img,result_dict = log_tool.process(image)
                push_image_to_redis(r,'101_50_0',result_img,result_dict,activate_step)
                
                
                
                if activate_step%20 == 0:
                    if not tc.check_on_line():
                        cv2.destroyAllWindows()
                        break
                    if not tc.check_activate():
                        cv2.destroyAllWindows()
                        print ('deactivate')
                        time.sleep(1)
                        print ('wait for activate...')
                        break
                
                if activate_step>10000000:
                    activate_step = 0
        
        
        if not tc.check_on_line():
            print ('person ReID server offline!')
            time.sleep(1)
            break
        
        #print (result_names)
        #cv2.imshow('Login Image', result_img)
        # 等待按键，如果按下'q'则退出循环  
        #if cv2.waitKey(1) & 0xFF == ord('q'):  
        #    break  
        
        #if push_count%30 == 0:
        #    if r.get('face_recognition_down')==b'1':
        #        break
    # 销毁所有OpenCV窗口  
    #cv2.destroyAllWindows()