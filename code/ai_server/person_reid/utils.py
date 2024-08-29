from ultralytics import RTDETR
import supervision as sv
import cv2
import torch
from torchvision import transforms
from PIL import Image
from torch.autograd import Variable
import pickle
import zlib
import numpy as np
import faiss
import os

from config import EnvConfig
from body_model import ft_net,load_network,fuse_all_conv_bn



def get_dir_files(path):
    return os.listdir(path)


#头 在 哪个身体里面
def get_xywh_in_xyxys_index(box,boxes):
    print('box',box)
    print('boxes',boxes)
    box_x = (2*box[0]+box[2])/2
    box_y = (2*box[1]+box[3])/2
    
    dist = 999999999
    result_index = -1
    index = 0
    for _ in boxes:
        this_x = (_[0]+_[2])/2
        this_y = (_[1]+_[3])/2
        if box_x>=_[0] and box_x<=_[2] and box_y>=_[1] and box_y<=_[3]:
            this_dist = (box_x-this_x)**2+(box_y-this_y)**2
            if this_dist<dist:
                dist = this_dist
                result_index = index
    return result_index

#保存特征
def save_feature2file(file_path,feature):
    serialized_data = zlib.compress(pickle.dumps(feature))
    with open(file_path, 'wb') as feature_file:
        feature_file.write(serialized_data)
    feature_file.close()

#读取特征    
def load_file2feature(file_path):
    with open(file_path, 'rb') as feature_file:
        compressed_data = feature_file.read()
    feature_file.close()
    uncompressed_data = pickle.loads(zlib.decompress(compressed_data))
    return uncompressed_data

def cut_box_from_img(pic_img,xyxy_box): #BGR img
    x1, y1, x2, y2 = xyxy_box
    # Ensure that the region does not exceed the bounds of pic_img
    x1 = max(0, x1)
    y1 = max(0, y1)
    x2 = min(x2, pic_img.shape[1])
    y2 = min(y2, pic_img.shape[0])
    return pic_img[y1:y2, x1:x2]

class BodyDetect:
    def __init__(self):
        self.env = EnvConfig()
        self.v8_model = RTDETR(self.env.detector_model_path)
    
    def body_detect(self,img_frame):  # ,v8_model,frame):
        self.body_detect_result = []
        results = self.v8_model(img_frame, imgsz=640)[0]
        results.obb = None
        #print ('********result:',results.boxes)
        try:
            detections = sv.Detections.from_ultralytics(results)
            # 选取置信度大于0.5的检测框
            detections = detections[(detections.confidence > 0.6)]  # [detections.class_id == 0,1]
            #face_boxes = detections[detections.class_id == 1]  # use in the feature
            body_boxes = detections[detections.class_id == 0]
        except Exception as e:
            print (e)
            return False
        if len(body_boxes)==0:
            print ('no body in img !')
            return False
        for i in range(len(body_boxes)):
            #print (body_boxes[i].xyxy.tolist())
            self.body_detect_result.append([int(num) for num in (body_boxes[i].xyxy[0])])
        return True



        
class BodyFeature:
    def __init__(self):
        self.env = EnvConfig()
        #self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu") # 单GPU或者CPU
        h, w = 256, 128
        self.data_transforms = transforms.Compose([
            transforms.Resize((h, w), interpolation=3),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        model_structure = ft_net(751, stride=2, ibn=False, linear_num=512)
        self.reid_model = fuse_all_conv_bn(load_network(model_structure,self.env.reid_model_path).eval().cuda())
    
    def fliplr(self,img):
        '''flip horizontal'''
        inv_idx = torch.arange(img.size(3) - 1, -1, -1).long()  # N x C x H x W
        img_flip = img.index_select(3, inv_idx)
        return img_flip 
    
    # 提取人体信息
    def extract_body_feature(self,img):
        linear_num = 751 #751维特征向量
        with torch.no_grad():
            img = Image.fromarray(img)
            img = self.data_transforms(img).unsqueeze(0)
            n, c, h, w = img.size()

            ff = torch.FloatTensor(n, linear_num).zero_().cuda()
            # 翻转图像增强
            for i in range(2):
                if (i == 1):
                    img = self.fliplr(img)
                input_img = Variable(img.cuda())

                outputs = self.reid_model(input_img)
                #print (outputs)
                ff += outputs
            # norm feature
            fnorm = torch.norm(ff, p=2, dim=1, keepdim=True)
            ff = ff.div(fnorm.expand_as(ff))
        return ff

    
class FeatureCompare:
    def __init__(self):
        self.body_db = None
  
    def build_body_db(self,features:list):
        features_np = np.array(features)
        print ("buid body database feature shape len:%d"%features_np.shape[1])
        self.body_db = faiss.IndexFlatL2(features_np.shape[1])  # 使用L2距离  
        self.body_db.add(features_np)  # 将向量添加到索引中
    
    def select_feature(self,feature):
        feature = np.array(feature)
        #print (feature.shape)
        k = 1  # 搜索最相似的1个向量  
        distances, labels = self.body_db.search(feature, k)  # 进行搜索
        return distances[0][0],labels[0][0]
    
        


if __name__ == "__main__":
    bodyd = BodyDetect()
    testpic = r"F:\workspace\majun\img\test.jpg"
    pic_img = cv2.imread(testpic)
    result = bodyd.body_detect(pic_img)
    print ("-----------------")
    print (bodyd.body_detect_result)
    
    #save img cut
    #i = 0
    #for box in bodyd.body_detect_result:
    #    cv2.imwrite(str(i)+".jpg",cut_box_from_img(pic_img,box))
    #    i+=1
    
    bodyf = BodyFeature()
    result = bodyf.extract_body_feature(pic_img)
    print (result.shape)


    #
    import faiss
    import numpy as np  
    
    # 假设向量维度为128，数据库大小为10000  
    d = 751 
    nb = 100
    np.random.seed(1234)  # 确保可重复性  
    xb = np.random.random((nb, d)).astype('float32')  # 生成10000个128维的随机向量

    print (xb.shape)

    index = faiss.IndexFlatL2(d)  # 使用L2距离  
    index.add(xb)  # 将向量添加到索引中

    if result.is_cuda:  
        result = result.cpu()  
    
    xq= np.array([result.squeeze(0).numpy()])
    print (xq.shape)
    #xq = np.random.random((1, d)).astype('float32')  # 生成一个查询向量  
    k = 1  # 搜索最相似的4个向量  
    distances, labels = index.search(xq, k)  # 进行搜索  
    
    print(distances)  # 输出相似度（距离）  
    print(labels)  # 输出相似向量的索引