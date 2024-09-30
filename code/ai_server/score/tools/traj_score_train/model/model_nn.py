import torch  
import torch.nn as nn  
import torch.optim as optim  
from torch.utils.data import Dataset, DataLoader  
from torchvision import transforms  
from PIL import Image  
import os  
import torch.nn.functional as F
import torchvision


import uuid

def generate_random_value(length):
    # 生成一个 UUID
    random_uuid = uuid.uuid4()
    # 将 UUID 转换为字符串，并去除其中的分隔符 '-'
    random_str = str(random_uuid).replace('-', '')
    # 截取指定长度的随机值
    random_value = random_str[:length]
    return random_value


# 定义神经网络模型  
class SimpleCNN(nn.Module):  
    def __init__(self):  
        super(SimpleCNN, self).__init__()  
        self.conv1 = nn.Conv2d(3, 6, 5)  
        self.pool = nn.MaxPool2d(2, 2)  
        self.conv2 = nn.Conv2d(6, 16, 5)  
        self.fc1 = nn.Linear(16 * 5 * 5, 120)  
        self.fc2 = nn.Linear(120, 84)  
        self.fc3 = nn.Linear(84, 3)  # 输出3个类别的概率  
  
    def forward(self, x):  
        x = self.pool(F.relu(self.conv1(x)))  
        x = self.pool(F.relu(self.conv2(x)))  
        x = x.view(-1, 16 * 5 * 5)  
        x = F.relu
        
# 定义神经网络模型
class ShapeNet(nn.Module):
    def __init__(self):
        super(ShapeNet, self).__init__()
        self.resnet = torchvision.models.resnet18(pretrained=True)  # 使用预训练的ResNet模型
        self.fc = nn.Linear(1000, 3)  # 输出层，将ResNet的输出转换为三种形状的相似度

    def forward(self, x):
        x = self.resnet(x)
        x = self.fc(x)
        return x
    
# 定义修改后的ResNet模型
class ModifiedResNet(torchvision.models.ResNet):
    def __init__(self):
        super(ModifiedResNet, self).__init__(block=torchvision.models.resnet.BasicBlock, layers=[2, 2, 2, 2], num_classes=3)
        # 修改第一层的输入通道数
        self.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)


class ModifiedResNet_norm(torchvision.models.ResNet):
    def __init__(self):
        # 调用父类的初始化方法
        #super(ModifiedResNet_norm, self).__init__(block=torchvision.models.resnet.BasicBlock, layers=[2, 2, 2, 2], num_classes=6)
        #super(ModifiedResNet_norm, self).__init__(block=torchvision.models.resnet.BasicBlock, layers=[2, 2, 2, 2], num_classes=5)
        super(ModifiedResNet_norm, self).__init__(block=torchvision.models.resnet.BasicBlock, layers=[2, 2, 2, 2], num_classes=2)
        # 修改第一层的输入通道数
        self.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
        # 添加一个 Sigmoid 层
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)

        # 在输出层添加 Sigmoid 层
        x = self.sigmoid(x)
        
        return x
    
    
# 定义数据预处理
data_transform = transforms.Compose([
    transforms.Grayscale(),  # 转换为灰度图
    #transforms.Resize((224, 224)),
    #transforms.Resize((64,64)),
    transforms.Resize((256,144)),
    transforms.ToTensor(),
    #transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) #RGB
    transforms.Normalize(mean=[0.485], std=[0.229])  # 因为是灰度图，只有一个通道，只需一个均值和一个标准差
])




if __name__=="__main__":
    name_str = generate_random_value(12)
    print (name_str)
    print (type(name_str))