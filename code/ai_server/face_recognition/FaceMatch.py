from config import EnvConfig
from keras.applications.imagenet_utils import preprocess_input
from keras_vggface.vggface import VGGFace
import numpy as np
import cv2
import pickle
import zlib
from utils import *

class FaceMatch:
    def __init__(self):
        
        self.env = EnvConfig()
        self.vgg_face_model = VGGFace(model='senet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')
        
        
    def get_img_vggface_feature(self,face_img):
        # 调整人脸区域大小为(224, 224)
        face_img_resized = cv2.resize(face_img, (224, 224))
        # 将图像转换为NumPy数组，并在适当的维度上添加批次维度
        face_array = np.expand_dims(face_img_resized, axis=0)
        # 预处理图像，使其与VGGFace模型兼容
        face_array = preprocess_input(face_array)
        # 获取图像的特征表示
        features = self.vgg_face_model.predict(face_array,verbose=0)
        feature = np.squeeze(features)
        return feature
    
    
    def get_file_feature(self,file_path):
        img = cv2.imread(file_path)
        return self.get_img_vggface_feature(img)
    
    def compare_feature_EulerDistance(self,feature1,feature2):
        return euler_distance(feature1,feature2)
    
    #保存特征
    def save_feature2file(self,file_path,feature):
        serialized_data = zlib.compress(pickle.dumps(feature))
        with open(file_path, 'wb') as feature_file:
            feature_file.write(serialized_data)
        feature_file.close()
    
    #读取特征    
    def load_file2feature(self,file_path):
        with open(file_path, 'rb') as feature_file:
            compressed_data = feature_file.read()
        feature_file.close()
        uncompressed_data = pickle.loads(zlib.decompress(compressed_data))
        return uncompressed_data
    
    def check_features_score(self,score):
        #if self.env.USE_MODEL == 'resnet': 
        #    if score>= self.env.resnet_same_face_cosine_similarity_threshold:
        #        return True
        #    else:
        #        return False
        #elif self.env.USE_MODEL=='vggface':
            if score<self.env.vggface_same_face_euler_distance_threshold:
                return True
            else:
                return False
    
    def compare_score_beyond_score(self,score1,score2):
        #if self.env.USE_MODEL == 'resnet': 
        #    return score1>score2
        #elif self.env.USE_MODEL=='vggface':
            return score1<score2
               
    def face_imgs_select(self,target_face,faces_feature_dict): 
        begin_flag = True
        best_score = None
        best_name = self.env.defeat_match_name
        #target_feature = self.get_img_feature(target_face)
        target_feature = self.get_img_vggface_feature(target_face)
        
        
        for face_id in faces_feature_dict.keys():
            face_feature = faces_feature_dict[face_id]['feature']
            
            
            #for face_feature in face_features:
            #this_score = self.evl_features(target_feature,face_feature)
            this_score = self.compare_feature_EulerDistance(target_feature,face_feature)
            if begin_flag:
                if self.check_features_score(this_score):
                    best_score = this_score
                    best_name = faces_feature_dict[face_id]['name']
                    begin_flag = False
            else:
                if self.compare_score_beyond_score(this_score,best_score):
                    best_score = this_score
                    best_name = faces_feature_dict[face_id]['name']
        return best_name    
    
if __name__ == "__main__":
    testpic = r"F:\workspace\majun\img\majun.png"
    from CutFace import CutFace
    cut_face = CutFace()
    pic_img = cv2.imread(testpic)
    face_boxes,face_imgs = cut_face.cut_faces_from_img(pic_img)
    
    
    fm = FaceMatch()
    feature = fm.get_img_vggface_feature(face_imgs[0])
    print(feature)
    