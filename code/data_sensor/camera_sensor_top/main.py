
import time
import cv2
import redis
import os
from redis_tools import push_image_to_redis,push_server_pid
from thread_controller import ThreadControler

class CameraSensor:
    def __init__(self,camera_num=0,width=1280,height=720):
        self.width = width
        self.height=height
        self.camera_num = camera_num
        self.redis_connect = redis.Redis(host='localhost', port=6379, db=0) 
    
        #capture
        self.cap = cv2.VideoCapture(self.camera_num)
        
    def init_camera(self):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)  
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        # 检查是否成功设置分辨率  
        if self.cap.get(cv2.CAP_PROP_FRAME_WIDTH) != self.width or self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) != self.height:  
            print(f"无法设置分辨率到 {self.width}x{self.height}")
            return False  
        else:  
            print(f"成功设置分辨率到 {self.width}x{self.height}")
            return True
        
    def capture(self,activate_step):
        # 逐帧读取摄像头捕捉的画面  
        ret, frame = self.cap.read()
        
        # 检查是否成功读取画面  
        if not ret:  
            print("无法接收帧（画面）。退出...")  
            return False
        
        # 显示画面  
        #cv2.imshow('frame', frame) 
        
        
        #2024.9.11
        push_image_to_redis(self.redis_connect,frame,activate_step)
        #push_jpg_image_to_redis(self.redis_connect,frame,activate_step)
        
        
        return True
        

if __name__ == '__main__':
    print ('top camera sensor server online!')
    r = redis.Redis(host='localhost', port=6379, db=0)
    
    
    time.sleep(0.3)
    tc = ThreadControler()
    tc.init_thread()
    
    
    pid = os.getpid()
    print(f"当前进程的PID是: {pid}")   
    push_server_pid(r,'ai_server_pid','camera_top',str(pid))
    
    print ('wait for activate...')
    while True:
        if not tc.check_activate():
            time.sleep(3)
        else:
            print ('top camera sensor activate')
            camera  = CameraSensor(camera_num=0) #majun 20241031
            if camera.init_camera():
                print ('camera ready')
            else:
                print ('camera fail!')
                time.sleep(2)
                break
            
            activate_step = 0
            while True:
                activate_step+=1
                flag = camera.capture(activate_step)
                if not flag:
                    print ('top camera something wrong!')
                    time.sleep(2)
                    break
            
                #print (activate_step)
                if activate_step%30 == 0:
                    if (not tc.check_on_line()) or (not tc.check_ai_online()):
                        #cv2.destroyAllWindows()
                        break
                    if not tc.check_activate():
                        #cv2.destroyAllWindows()
                        print ('deactivate')
                        time.sleep(1)
                        print ('wait for activate...')
                        break
            
                if activate_step>10000000:
                    activate_step = 0
        
        if (not tc.check_on_line()) or (not tc.check_ai_online()):
            print ('top camera sensor server offline!')
            time.sleep(1)
            break
        
