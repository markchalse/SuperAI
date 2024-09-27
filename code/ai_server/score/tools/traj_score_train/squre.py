from draw_utils import pil_draw_pic
import numpy as np
import random
import cv2

width = 1280
height = 720

def draw_square(point_number,noise_scale): # noise_scale 0~1


    # 定义正方形的边长  
    side_length = int(point_number/4)

    # 生成正方形四个边上的点的坐标  
    x_top = np.linspace(-side_length/2, side_length/2, num=side_length)  
    y_top = np.full_like(x_top, side_length/2)  
    
    x_bottom = np.linspace(-side_length/2, side_length/2, num=side_length)  
    y_bottom = np.full_like(x_bottom, -side_length/2)  
    
    x_left = np.full_like(y_top, -side_length/2)  
    y_left = np.linspace(-side_length/2, side_length/2, num=side_length)  
    
    x_right = np.full_like(y_top, side_length/2)  
    y_right = np.linspace(-side_length/2, side_length/2, num=side_length)  
    
    # 合并所有边的点的坐标  
    x_all = np.concatenate((x_top, x_right[1:], x_bottom[::-1], x_left[::-1][1:]))  
    y_all = np.concatenate((y_top, y_right[1:], y_bottom[::-1], y_left[::-1][1:]))  


    # 添加轻微的随机噪音到每个点的坐标  
    #noise_scale = 0.075  # 控制噪音的大小  
    noise_scale = noise_scale*0.13+0.065
    x_all_noisy = x_all + np.random.normal(0, noise_scale, size=x_all.size)  
    y_all_noisy = y_all + np.random.normal(0, noise_scale, size=y_all.size)
    return x_all_noisy, y_all_noisy

if __name__ == '__main__':
    x,y = draw_square(100,random.random())
    print (x)
    img = pil_draw_pic(width,height,x,y)
    img = img[:, :, ::-1]  
    cv2.imwrite('test.jpg',img)