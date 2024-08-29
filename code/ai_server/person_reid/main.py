import redis
import os

from utils import *
from redis_tools import *
from config import EnvConfig
from thread_controller import ThreadControler

class PersonReID:
    def __init__(self):
        self.env = EnvConfig()
        self.redis_connect = redis.Redis(host='localhost', port=6379, db=0)
        self.body_find = BodyDetect()
        self.feature_tool = BodyFeature()
        #self.person_name_list = []
        self.feature_compare = FeatureCompare()
        self.match_tool = BestMatch()
        
    
    def init_feature_compare(self):
        self.match_tool = BestMatch()
        all_features = []
        feature_files = os.listdir(self.env.body_features_path)
        for feature_file in feature_files:
            if '.body_f' not in feature_file:
                continue
            student_name = feature_file.split('_')[0]
            #print (student_name)
            #self.person_name_list.append(student_name)
            self.match_tool.name_list.append(student_name)
            feature_data = load_file2feature(os.path.join(self.env.body_features_path,feature_file))
            if feature_data.is_cuda:
                feature_data = feature_data.cpu()
            feature_data = feature_data.squeeze(0).numpy()
            all_features.append(feature_data)
        if len(all_features)>0:
            self.feature_compare.build_body_db(all_features)
            
        
    def start(self,step_count):
        self.match_tool.clear_result()
        camera_img,capture_time = get_image_from_redis(self.redis_connect,self.env.camera_redis_key)
        if camera_img is not None:          
            #cv2.imshow('Image from Redis', camera_img)
            result = self.body_find.body_detect(camera_img)
            #print ("-----------------")
            #print (self.body_find.body_detect_result)
            for body_box in self.body_find.body_detect_result:
                body_img = cut_box_from_img(camera_img,body_box)
                #cv2.imshow('Image from Redis', body_img)
                body_feature = self.feature_tool.extract_body_feature(body_img)
                if body_feature.is_cuda:
                    body_feature = body_feature.cpu()
                body_feature = body_feature.squeeze(0).numpy()
                d,index = self.feature_compare.select_feature([body_feature])
                #print (index,d)
                self.match_tool.best_match_index.append(index)
                self.match_tool.distance.append(d)
                self.match_tool.boxes.append(body_box)
            
            #校准 避免匹配同一个人
            self.match_tool.calibration()
            
            #print (self.match_tool.best_match_index)
            result_img  = np.array(camera_img)
            result_dict = {}
            for bm_i in range(len(self.match_tool.best_match_index)):
                if self.match_tool.best_match_index[bm_i] == -1:
                    continue
                x = self.match_tool.boxes[bm_i][0]
                y = self.match_tool.boxes[bm_i][1]
                x_ = self.match_tool.boxes[bm_i][2]
                y_ = self.match_tool.boxes[bm_i][3]
                try:
                    cv2.rectangle(result_img, (x, y), (x_, y_), (0,255,0), self.env.face_line_width)
                    cv2.putText(result_img, self.match_tool.name_list[self.match_tool.best_match_index[bm_i]], \
                        (x, y-self.env.face_line_width), cv2.FONT_HERSHEY_SIMPLEX, self.env.text_size, (0,255,0), self.env.face_name_size)
                except Exception as e:
                    print (e)
                result_dict[self.match_tool.name_list[self.match_tool.best_match_index[bm_i]]] = {}
                result_dict[self.match_tool.name_list[self.match_tool.best_match_index[bm_i]]]['name'] = self.match_tool.name_list[self.match_tool.best_match_index[bm_i]]
                result_dict[self.match_tool.name_list[self.match_tool.best_match_index[bm_i]]]['box'] = self.match_tool.boxes[bm_i]
                push_image_to_redis(self.redis_connect,self.env.person_reid_key,result_img,result_dict,step_count)
            cv2.imshow('Image from Redis', result_img)    
            if cv2.waitKey(1) & 0xFF == ord('q'):  
                return

  
class BestMatch:
    def __init__(self):
        self.name_list = []
        self.best_match_index = []
        self.distance = []
        self.boxes = []
    
    
    def init_name(self,name_list):
        self.name_list = name_list
    
    def clear_result(self):
        self.best_match_index = []
        self.distance = []
        self.boxes = []
    
    def calibration(self):
        for bm_i in range(len(self.best_match_index)):
            if self.best_match_index[bm_i]==-1:
                continue
            #绝对距离检测，差异太离谱的就out了  1.25经验值
            if self.distance[bm_i]>1.25:
                self.best_match_index[bm_i] = -1
                continue
            for target_i in range(len(self.best_match_index)):  
                if target_i == bm_i or self.best_match_index[target_i]==-1:
                    continue
                if self.name_list[self.best_match_index[target_i]] == self.name_list[self.best_match_index[bm_i]]:
                    if self.distance[bm_i]<self.distance[target_i]:
                        self.best_match_index[target_i] = -1
                    else:
                        self.best_match_index[bm_i] = -1
                        break

if __name__ == "__main__":
    '''
    bodyf = BodyFeature()
    
    #testpic = r"F:\workspace\majun\img\ma.jpg"
    #testpic = r"F:\workspace\majun\img\lan.jpg"
    testpic = r"F:\workspace\majun\img\test_ma.jpg"
    pic_img = cv2.imread(testpic)
    result = bodyf.extract_body_feature(pic_img)
    #save_feature2file('ma.data',result)
    #save_feature2file('lan.data',result)
    
    bodys = []
    ma = load_file2feature('ma.data')
    if ma.is_cuda:
        ma = ma.cpu()
    ma = ma.squeeze(0).numpy()
        
    
    lan = load_file2feature('lan.data')
    if lan.is_cuda:
        lan = lan.cpu()
    lan = lan.squeeze(0).numpy()
    
    bodys.append(lan)
    bodys.append(ma)
    
    #print (bodys)
    
    fc  =FeatureCompare()
    fc.build_body_db(bodys)
    
    
    if result.is_cuda:
        result = result.cpu()
    result = result.squeeze(0).numpy()
    d,index = fc.select_feature([result])
    
    print (d,index)
    '''
    
    
    print ('person ReID server online!')
    time.sleep(0.3)
    tc = ThreadControler(EnvConfig(server='person_reid'))
    tc.init_thread()
    print ('wait for activate...')
    
    while True:
        if not tc.check_activate():
            time.sleep(3)
        else:
            p_reid=PersonReID()
            p_reid.init_feature_compare()
            activate_step = 0
            while True:
                activate_step+=1
                p_reid.start(activate_step)
                
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
    
    cv2.destroyAllWindows()