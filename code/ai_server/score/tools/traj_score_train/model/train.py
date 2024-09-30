import torch
from torch.utils.data import Dataset, DataLoader  
from PIL import Image  
import os
from torchvision import transforms 
import torch.nn as nn  
import torch.optim as optim  

import torchvision


from model_nn import SimpleCNN
from model_nn import ShapeNet
from model_nn import data_transform
from model_nn import ModifiedResNet
from model_nn import ModifiedResNet_norm

from tqdm import tqdm
#import sys
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from TrajModelconfig import EnvConfig

import numpy as np 
from PIL import Image, ImageDraw
import cv2

def pil_draw_pic(width,height,trajectory_x,trajectory_y):
    #print ('--------------pil_draw_pic---------------')
    #print ('trajectory length:',len(trajectory_x))
    # 设定图像大小  
    #width, height = 640, 640
    # 创建一个新的空白图像，大小为width x height，背景色为自定义颜色  
    rgb_tuple = (50, 61, 76)  # 自定义背景色  
    image = Image.new('RGB', (width, height), color=rgb_tuple)  
      
    
    if len(trajectory_x)==0:
        # 将PIL图像转换为OpenCV图像格式  
        image_np = np.array(image)  
        #image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)  
        #print (image_np.shape)
        # 返回OpenCV图像  
        print ('--------------pil_draw_pic---------------')
        print ('empty trajectory!')
        return image_np 
    
    
    # 创建一个可以在图像上绘制的对象  
    draw = ImageDraw.Draw(image)  
    
    
    x_coords = [ x*width*0.9 for x in trajectory_x] 
    y_coords = [ (1-y)*height*0.9 for y in trajectory_y] 
    #middle_x = 0.5*width
    #middle_y = 0.5*height
    
    
    #x_coords = [ (x-middle_x)*boom_size + middle_x for x in x_coords_]
    #y_coords = [ (y-middle_y)*boom_size + middle_y for y in y_coords_]
    
    
    # 绘制轨迹线  
    rgb_tuple = (13, 113, 201)  # 轨迹线颜色  
    draw.line(list(zip(x_coords, y_coords)), fill=rgb_tuple, width=5)  
      
    # 绘制轨迹点  
    for x, y in zip(x_coords, y_coords):  
        draw.ellipse((x-8, y-8, x+8, y+8), fill=rgb_tuple)  
      
    # 绘制终点标记  
    last_x, last_y = x_coords[-1], y_coords[-1]  
    draw.ellipse((last_x-15, last_y-15, last_x+15, last_y+15), fill=rgb_tuple)  
    draw.ellipse((last_x-6, last_y-6, last_x+6, last_y+6), fill=(255, 255, 255))  
      
    # 将PIL图像转换为OpenCV图像格式  
    image_np = np.array(image)  
    #image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)  
    #print (image_np.shape)
    # 返回OpenCV图像  
    return image_np 


env = EnvConfig()


'''
# 数据预处理  
transform = transforms.Compose([  
    transforms.Resize((64, 64)),  # 假设所有图片调整为64x64大小  
    transforms.ToTensor(),  
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))  # 归一化  
])

# 自定义数据集类  
class ShapeDataset(Dataset):  
    def __init__(self, root_dir, transform=None):  
        self.transform = transform  
        self.classes = ['circle', 'rectangle', 'triangle']  
        self.class_to_idx = {cls_name: i for i, cls_name in enumerate(self.classes)}  
        self.samples = []  
        for cls_name in self.classes:  
            cls_dir = os.path.join(root_dir, cls_name)  
            for file_name in os.listdir(cls_dir):  
                path = os.path.join(cls_dir, file_name)  
                self.samples.append((path, self.class_to_idx[cls_name]))  
  
    def __len__(self):
        return len(self.samples)  
  
    def __getitem__(self, idx):  
        path, target = self.samples[idx]  
        image = Image.open(path).convert('RGB')  
        if self.transform:  
            image = self.transform(image)  
        return image, torch.tensor(target, dtype=torch.long)  


# 创建数据集和数据加载器  
dataset = ShapeDataset(root_dir='D:\\majun\\image\\image_score\\train', transform=transform)  
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

# 实例化模型  
model = SimpleCNN()  
  
# 定义损失函数和优化器  
criterion = nn.NLLLoss()  # 负对数似然损失，用于多分类  
optimizer = optim.Adam(model.parameters(), lr=0.001)  
  
# 训练模型  
num_epochs = 10  
for epoch in range(num_epochs):  
    running_loss = 0.0  
    for i, data in enumerate(dataloader, 0):  
        inputs, labels = data 
        optimizer.zero_grad()  
  
        # 前向传播  
        outputs = model(inputs)  
        loss = criterion(outputs, labels)  
  
        # 反向传播和优化  
        loss.backward()  
        optimizer.step()  
  
        # 打印统计信息  
        running_loss += loss.item()  
        if i % 2000 == 1999:  # 每2000个mini-batches打印一次  
            print('[%d, %5d] loss: %.3f' %  
                  (epoch + 1, i + 1, running_loss / 2000))  
            running_loss = 0.0  
  
print('Finished Training')  
  
# 保存模型  
torch.save(model.state_dict(), 'model.pth')
'''


# 检查是否有可用的GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")



# 加载数据集
train_dataset = torchvision.datasets.ImageFolder(root=env.train_base_path, transform=data_transform)
train_loader = DataLoader(train_dataset, batch_size=env.batch_size, shuffle=True)

# 初始化模型和优化器
#model = ShapeNet().to(device)
#model = ModifiedResNet().to(device)
model = ModifiedResNet_norm().to(device)

optimizer = optim.Adam(model.parameters(), lr=env.learning_rate)
#criterion = nn.MSELoss()  # 使用均方误差损失函数
#criterion = nn.CrossEntropyLoss()  # 使用交叉熵损失函数，因为输出是类别
criterion = nn.BCEWithLogitsLoss()  # 使用二元交叉熵损失函数



# 标签映射到 one-hot 编码
'''
label_map = {
    "circle": torch.tensor([1, 0, 0, 0 , 0,0], dtype=torch.float).to(device),
    "square": torch.tensor([0, 1, 0 , 0 , 0,0], dtype=torch.float).to(device),
    "triangle": torch.tensor([0, 0, 1,0 , 0,0], dtype=torch.float).to(device),
    "straight_line": torch.tensor([0, 0, 0,1 , 0,0], dtype=torch.float).to(device),
    "random": torch.tensor([0, 0, 0,0 , 1,0], dtype=torch.float).to(device),
    "rectangle": torch.tensor([0, 0, 0,0 , 0,1], dtype=torch.float).to(device),
}
'''

'''
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


show_x = []
show_y = []


# 训练模型
num_epochs = env.epoch
for epoch in range(num_epochs):
    running_loss = 0.0
    bar = tqdm(total=len(train_loader))
    for images, labels in train_loader:
        #print (labels)
        # 将数据移动到GPU上
        images, labels = images.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(images)
        
        # 扩展目标张量的维度，使其与模型输出的形状相匹配
        #labels = labels.unsqueeze(1).float()
        
        # 将类别索引转换为 one-hot 编码
        one_hot_labels = torch.stack([label_map[train_dataset.classes[label_idx]] for label_idx in labels])
        
        #loss = criterion(outputs, labels)  # 计算损失
        loss = criterion(outputs, one_hot_labels)  # 计算损失
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
        bar.update(1)
    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(train_loader)}")
    
    show_x.append((epoch+1)/num_epochs)
    show_y.append(running_loss/len(train_loader))
    loss_img = pil_draw_pic(640,640,show_x,show_y)
    loss_img = loss_img[:, :, ::-1]  
    cv2.imshow('loss_img', loss_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  
        break

# 保存模型
torch.save(model.state_dict(), os.path.join(env.model_save_path,"score_model.pth"))
# 销毁所有OpenCV窗口  
cv2.destroyAllWindows()