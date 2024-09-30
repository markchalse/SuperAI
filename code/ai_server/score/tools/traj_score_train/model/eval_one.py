import cv2
import torch
from torchvision import transforms
from PIL import Image
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from TrajModelconfig import EnvConfig

from model_nn import ModifiedResNet
from model_nn import data_transform
from model_nn import ModifiedResNet_norm


class ScoreEval():

    def __init__(self):
        self.env = EnvConfig()

        # 检查是否有可用的GPU
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # 加载模型
        #model = ModifiedResNet().to(device)
        self.model = ModifiedResNet_norm().to(self.device)
        self.model.load_state_dict(torch.load(os.path.join(self.env.model_save_path,"score_model.pth")))
        self.model.eval()

        # 定义形状名称
        #self.shape_names = ['Circle', 'Square', 'Triangle']
        #self.shape_names = ['Square', 'Triangle']
        self.shape_names = ['矩形', '三角形']
        
        
    def get_score_from_image(self,image):
        # 将图像转换为 PIL 图像
        image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        # 预处理图像并将其转换为模型输入所需的格式
        input_image = data_transform(image_pil).unsqueeze(0).to(self.device)  # 添加一个维度并将其移动到GPU上
        
        # 使用模型进行预测
        with torch.no_grad():
            outputs = self.model(input_image)
            
            _, predicted = torch.max(outputs, 1)
            predicted_class = self.shape_names[predicted.item()]
            
            result_list = outputs.squeeze().tolist()  # 将输出张量转换为 Python 列表

        #print("Predicted shape:", predicted_class)
        #print("result_list:",result_list)
        
        return result_list,predicted_class
        


if __name__ == "__main__":
    se = ScoreEval()

    # 读取图像
    image_path = "test3.jpg"
    #image_path = "test.jpg"
    image = cv2.imread(image_path)
    
    
    
    scores,item = se.get_score_from_image(image)

    print("Predicted shape:", item)
    print("result scores:",scores)


