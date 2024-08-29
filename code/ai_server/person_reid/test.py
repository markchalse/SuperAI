#pip install faiss -i https://pypi.tuna.tsinghua.edu.cn/simple/
#conda install -c faiss-gpu
import torch
from scipy import optimize
import numpy as np

def features_2_tensors(features_list:list):
    feature_len = 3#751
    features = torch.zeros([len(features_list), feature_len])
    for i in range(len(features_list)):
        features[i,:] = features_list[i]
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu") # 单GPU或者CPU
    features = features.to(device)
    return features

# 基于相似度的匈牙利
def id_matcher(body_feats,group_id_feature):
    query = body_feats.T
    print(query.shape)
    print (group_id_feature.shape)
    score = torch.mm(group_id_feature, query)
    print (score.shape)
    print (score)
    score = score.squeeze(1).cpu()
    score = 1 - score.detach().numpy()
    score = score.T #mark20240411
    print (score)
    #print (score.T)
    #score = score.T
    #print (score)
    mem_ind, col_ind = optimize.linear_sum_assignment(score)
    print (mem_ind,col_ind)
    print(score[mem_ind,col_ind ].sum())
    #print(mem_ind[1])
    
    ###mark check
    #for pi in range(len(mem_ind)):
    #    if score[pi][mem_ind[pi]] >0.1:
    #        mem_ind[pi] = -1
    
    ###mark check
    
    #return mem_ind.tolist()#mark20240411
    return mem_ind.tolist(),col_ind.tolist()#mark20240411 #mem_ind行索引检测画面中的身体  列索引库中身体



#a = features_2_tensors(np.array([[1,2,3],[5,4,3]]))
#b = features_2_tensors([[1,2.2,3]])

a= torch.FloatTensor([[1,2,3],[5,4,3]])
b= torch.FloatTensor([[1,2.2,3],[6.1,5.2,4.3]])

c,d = id_matcher(b,a)


import faiss
import numpy as np  
  
# 假设向量维度为128，数据库大小为10000  
d = 128  
nb = 10000  
np.random.seed(1234)  # 确保可重复性  
xb = np.random.random((nb, d)).astype('float32')  # 生成10000个128维的随机向量

print (xb.shape)

index = faiss.IndexFlatL2(d)  # 使用L2距离  
index.add(xb)  # 将向量添加到索引中


xq = np.random.random((1, d)).astype('float32')  # 生成一个查询向量  
k = 1  # 搜索最相似的4个向量  
distances, labels = index.search(xq, k)  # 进行搜索  
  
print(distances)  # 输出相似度（距离）  
print(labels)  # 输出相似向量的索引