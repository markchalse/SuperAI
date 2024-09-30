import torch
import torchvision
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

from model_nn import ShapeNet
from model_nn import data_transform
from model_nn import ModifiedResNet
from model_nn import ModifiedResNet_norm

from tqdm import tqdm

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from TrajModelconfig import EnvConfig


env = EnvConfig()


# 检查是否有可用的GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")



# 加载测试数据集
test_dataset = torchvision.datasets.ImageFolder(root=env.test_base_path, transform=data_transform)
test_loader = DataLoader(test_dataset, batch_size=env.batch_size, shuffle=False)


# 加载保存的模型
#model = ShapeNet().to(device)
#model = ModifiedResNet().to(device)
model = ModifiedResNet_norm().to(device)
model.load_state_dict(torch.load(os.path.join(env.model_save_path,"score_model.pth")))
model.eval()

# 定义形状名称
#shape_names = ['circle', 'square', 'triangle']


'''
# 标签映射到 one-hot 编码
label_map = {
    "circle": torch.tensor([1, 0, 0, 0 , 0,0], dtype=torch.float).to(device),
    "square": torch.tensor([0, 1, 0 , 0 , 0,0], dtype=torch.float).to(device),
    "triangle": torch.tensor([0, 0, 1,0 , 0,0], dtype=torch.float).to(device),
    "straight_line": torch.tensor([0, 0, 0,1 , 0,0], dtype=torch.float).to(device),
    "random": torch.tensor([0, 0, 0,0 , 1,0], dtype=torch.float).to(device),
    "rectangle": torch.tensor([0, 0, 0,0 , 0,1], dtype=torch.float).to(device),
}

label_map = {
    "circle": torch.tensor([1, 0, 0, 0 , 0], dtype=torch.float).to(device),
    "square": torch.tensor([0, 1, 0 , 0 , 0], dtype=torch.float).to(device),
    "triangle": torch.tensor([0, 0, 1,0 , 0], dtype=torch.float).to(device),
    "straight_line": torch.tensor([0, 0, 0,1 , 0], dtype=torch.float).to(device),
    #"random": torch.tensor([0, 0, 0,0 , 1,0], dtype=torch.float).to(device),
    "rectangle": torch.tensor([0, 0, 0,0 ,1], dtype=torch.float).to(device),
}
'''

label_map = {
    "square": torch.tensor([1, 0], dtype=torch.float).to(device),
    "isosceles_right_triangle": torch.tensor([0, 1], dtype=torch.float).to(device),
}


all_out_param = []

# 测试模型
correct = 0
total = 0

bar = tqdm(total = len(test_loader))
with torch.no_grad():
    
    for images, labels in test_loader:
        #print ('labels',labels)
        images, labels = images.to(device), labels.to(device)
        
        
        #0425
        one_hot_labels = torch.stack([label_map[test_dataset.classes[label_idx]] for label_idx in labels])
        #print (labels)
        #print (one_hot_labels)
        
        outputs = model(images)
        #print (outputs)
        #print (outputs.shape)
        #_, predicted = torch.max(outputs, 1)#0425
        _, predicted_indices = torch.max(outputs, 1) 
        #print (predicted_indices)
        #print ('predicted',predicted)
        # 将one-hot编码的labels转换回索引形式  
        labels = torch.argmax(one_hot_labels, dim=1)
        #print (labels)
        total += labels.size(0)
        #correct += (predicted == labels).sum().item()#0425
        correct += (predicted_indices == labels).sum().item()
        for out in outputs:
            for _ in out:
                all_out_param.append(_)
    
        bar.update(1)

print(f"Accuracy on the test set: {100 * correct / total:.2f}%")

print ('max_value:',max(all_out_param),"  min_value:",min(all_out_param))

