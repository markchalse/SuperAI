from draw_utils import pil_draw_pic,vertices2list
import numpy as np
import random
import cv2
import math

width = 1280
height = 720
param = 0.7
workspace = r"F:\majun\img\traj_img\train\square"

def rotate_point(x, y, xc, yc, theta):  
    # 将点(x, y)围绕点(xc, yc)旋转theta弧度  
    # 计算旋转后的坐标  
    x_rotated = xc + math.cos(theta) * (x - xc) - math.sin(theta) * (y - yc)  
    y_rotated = yc + math.sin(theta) * (x - xc) + math.cos(theta) * (y - yc)  
    return x_rotated, y_rotated  
  
def rotate_square(vertices, theta):  #theta : 0-360 degrees
    theta = math.radians(theta)  # 将角度转换为弧度  
    
    # 假设vertices是一个包含四个顶点的列表，每个顶点是一个(x, y)元组  
    # 计算中心点的坐标  
    xc = sum(v[0] for v in vertices) / 4  
    yc = sum(v[1] for v in vertices) / 4  
      
    # 将每个顶点围绕中心点旋转theta弧度  
    rotated_vertices = [rotate_point(v[0], v[1], xc, yc, theta) for v in vertices]  
      
    return rotated_vertices 

def generate_square_vertices(width, height, param):  
    # 确定正方形的边长（假设边长范围是[1, min(width, height)])  
    side_length = random.randint(50, int(param*min(width, height)))  
      
    # 确定正方形的左上角坐标  
    x = random.randint(int((1-param)*width), width - side_length)  
    y = random.randint(int((1-param)*height), height - side_length)  
    
    len = int(0.5*side_length)
      
    # 计算四个顶点的坐标  
    vertices = [(x-len, y-len), (x+len, y-len), (x +len, y + len), (x-len, y + len)]  
      
    return vertices  

def inside_points(x_list,y_list,inside_num):
    res_x = []
    res_y = []
    for i in range(len(x_list)):
        x = x_list[i]
        y = y_list[i]
        if i == len(x_list)-1:
            x_=x_list[0]   
            y_=y_list[0]
        else:
            x_=x_list[i+1]
            y_=y_list[i+1]
        x_dist = x_-x
        y_dist = y_-y_list[i]
        res_x.append(x)
        res_y.append(y)
        for j in range(inside_num):
            res_x.append(x+(j/inside_num)*x_dist)
            res_y.append(y+(j/inside_num)*y_dist)
        res_x.append(x_)
        res_y.append(y_)
    return res_x,res_y
         

if __name__ == '__main__':
    
    
    pic_num = 0
    MAX_NUM = 500
    for i in range(MAX_NUM):
        print ('pic_num:',pic_num)
        
        points = generate_square_vertices(width,height,0.6)
        
        for theta_split in range(12):
            
            rotated_vertices = rotate_square(points, (theta_split-1)*30)  
            x,y =  vertices2list(rotated_vertices)
            x,y =  inside_points(x,y,40)
            img = pil_draw_pic(width,height,x,y)
            img = img[:, :, ::-1]  
            cv2.imwrite(f'{workspace}/square_{pic_num}.jpg',img)
            pic_num += 1 
        