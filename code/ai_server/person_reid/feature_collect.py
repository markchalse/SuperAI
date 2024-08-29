from config import EnvConfig
from utils import *
from redis_tools import *
from thread_controller import ThreadControler

class FeatureCollect:
    def __init__(self):
        self.env = EnvConfig()
        self.redis_connect = redis.Redis(host='localhost', port=6379, db=0)
        self.body_find = BodyDetect()
        self.feature_tool = BodyFeature()
        self.person_db = {}
        
        
    def start(self):
        print('------------------------------------------------------')
        persons,person_time = get_name_boxes_from_redis(self.redis_connect,self.env.face_recognition_redis_key)
        print (persons,person_time)
        capture_image,capture_time = get_image_from_redis(self.redis_connect,self.env.camera_redis_key)
        if capture_image is not None:  
            #print("No image available from Redis.")  
            #continue  
                              
            #cv2.imshow('Image from Redis', capture_image)  
                        
            self.body_find.body_detect(capture_image)
            for person_name in persons.keys():
                if person_name not in self.person_db.keys():
                    self.person_db[person_name] = {'feature_num':0,'feature_file':[]}
                if self.person_db[person_name]['feature_num'] > self.env.feature_max_count:
                    self.person_db[person_name]['feature_num'] = 0
                    continue
                body_index = get_xywh_in_xyxys_index(persons[person_name]['box'],self.body_find.body_detect_result)
                if body_index!=-1:
                    print ('body_index:',body_index)
                    print (self.body_find.body_detect_result[body_index])
                    body_img = cut_box_from_img(capture_image,self.body_find.body_detect_result[body_index])
                    cv2.imshow('body Image', body_img)
                    file_name = person_name+'_'+str(self.person_db[person_name]['feature_num'])+'.body_f'
                    save_feature2file(os.path.join(self.env.body_features_path,file_name),self.feature_tool.extract_body_feature(body_img))
                    self.person_db[person_name]['feature_num']+=1
                    
            if cv2.waitKey(1) & 0xFF == ord('q'):  
                return

    # 等待按键，如果按下'q'则退出循环  
    #if cv2.waitKey(1) & 0xFF == ord('q'):  
    #    break  

if __name__ == "__main__":
    print ('person feature collect server online!')
    tc = ThreadControler(env=EnvConfig(server='feature_collect'))
    tc.init_thread()
    
    print ('wait for activate...')
    
    while True:
        if not tc.check_activate():
            time.sleep(3)
        else:
            fc= FeatureCollect()
            #for i in range(50):
            activate_step = 0
            while True:
                fc.start()

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
            print ('person feature collect server offline!')
            time.sleep(1)
            break
    # 销毁所有OpenCV窗口  
    cv2.destroyAllWindows()