

from ultralytics import YOLO
import torch
from config import EnvConfig
import numpy as np

class StartTrack:
    def __init__(self):
        self.env = EnvConfig()
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.yolo = YOLO(self.env.yolo_model_check_point)
    
    #def get_yolo_results(self,source):
    #    results = self.yolo.predict(source,stream=False,device=self.device)
    #    return results
    
    def get_tracker_results(self,source):
        yolo_res = self.yolo.predict(source,stream=False,device=self.device,verbose=False) #verbose=False 关闭yolo回显    
        all_res = yolo_res[0].boxes.data.cpu().numpy()
        if len(all_res)==0:
            return []
        max_index = np.argmax(all_res[:, 4])  
        max_row = all_res[max_index]
        if max_row[4]<self.env.obj_confidence:
            return []
        return max_row[0:4]
        
        

if __name__ == "__main__":
    st = StartTrack()
    #yolo_res = st.get_yolo_results('test.png')
    tracker_res = st.get_tracker_results('test.png')
    #print(yolo_res)
    print(tracker_res)