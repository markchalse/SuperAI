

import cv2
import redis
from redis_tools import push_image_to_redis

if __name__ == '__main__':
    push_count = 0
    ###################### capture ##############
    #redis
    redis_connect = redis.Redis(host='localhost', port=6379, db=0) 
    redis_connect.set('camera_down','0')
    
    # 打开摄像头，参数0表示使用默认的摄像头  
    #cap = cv2.VideoCapture(self.env.CAMERA_NUM)  
    cap = cv2.VideoCapture(0)  
    # 检查摄像头是否成功打开  
    if not cap.isOpened():  
        print("无法打开摄像头")  
        exit()
    # 尝试设置分辨率，例如： 1920x1080 1280x720  
    width = 1280#1280 #1920 #1280  
    height = 720#720 #1080 #720  
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)  
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    # 检查是否成功设置分辨率  
    if cap.get(cv2.CAP_PROP_FRAME_WIDTH) != width or cap.get(cv2.CAP_PROP_FRAME_HEIGHT) != height:  
        print(f"无法设置分辨率到 {width}x{height}")  
    else:  
        print(f"成功设置分辨率到 {width}x{height}")  
    ###################### capture ##############
    
    while True:
        # 逐帧读取摄像头捕捉的画面  
        ret, frame = cap.read()
        
        # 检查是否成功读取画面  
        if not ret:  
            print("无法接收帧（画面）。退出...")  
            break
        
        # 显示画面  
        #cv2.imshow('frame', frame) 
        push_count = push_image_to_redis(redis_connect,frame,push_count)
        
        
        # 如果按下 'q' 键，则退出循环  
        if cv2.waitKey(1) & 0xFF == ord('q'):  
            break
        
        if push_count%30 == 0:
            if redis_connect.get('camera_down')==b'1':
                break
        
    # 释放摄像头并关闭所有OpenCV窗口  
    cap.release()  
    cv2.destroyAllWindows() 