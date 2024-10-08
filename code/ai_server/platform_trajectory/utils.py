import numpy as np 
from PIL import Image, ImageDraw

def str_array2np_array_float(str_array):
    # 移除字符串两端的方括号  
    cleaned_str = str_array[1:-1]  
    # 使用空格分割字符串，得到每个元素的字符串表示  
    elements_str = cleaned_str.split()  
    # 将每个元素的字符串表示转换为浮点数  
    elements_float = [float(x) for x in elements_str]  
    # 使用NumPy的array函数将列表转换为数组  
    array_back = np.array(elements_float)  
    #print(array_back)  
    return array_back


def pil_draw_pic(width,height,trajectory_x,trajectory_y,boom_size):
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
    
    
    
      
    # 转换轨迹坐标以适应图像大小  
    #x_fix_size = 0.6
    #y_fix_size = 0.6
    
    
    boom_size = boom_size
    traj_x_max = max(trajectory_x)
    traj_x_min =min(trajectory_x)
    x_middle = (traj_x_max-traj_x_min)/2.0+traj_x_min
    traj_y_max =max(trajectory_y)
    traj_y_min = min(trajectory_y)
    y_middle = (traj_y_max-traj_y_min)/2.0+traj_y_min
    x_traj_size = traj_x_max - traj_x_min
    y_traj_size = traj_y_max - traj_y_min
    
    x_bak = (x_middle-traj_x_min)*boom_size + traj_x_min - x_middle
    y_bak = (y_middle-traj_y_min)*boom_size + traj_y_min - y_middle
    
    
    x_coords = [x *width for x in trajectory_x]  
    y_coords = [y * height for y in trajectory_y]
    
    x_coords = trajectory_x
    y_coords = trajectory_y
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



class Trajectory:
    def __init__(self):
        
        self.trajx = []
        self.trajy = []