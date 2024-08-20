import numpy as np
import cv2

def cosin_metric(x1, x2):
    return np.dot(x1, x2) / (np.linalg.norm(x1) * np.linalg.norm(x2))

def euler_distance(a, b):
    # 归一化特征向量
    a = a / np.linalg.norm(a)
    b = b / np.linalg.norm(b)

    #欧拉距离
    return np.linalg.norm(a - b) 

def ImageArray2Cv2Image(image_array):
    bgr_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
    return bgr_image


def Cv2Image2ImageArray(cv2_array):
    gbr_image = cv2.cvtColor(cv2_array, cv2.COLOR_BGR2RGB)
    return gbr_image


def detect_image_channels(img):
    if img.size == 0:
        return 'ERROR'
    height, width, channels = img.shape
    if channels ==1:
        return 'GRAY'
    if channels != 3:
        return 'ERROR'
    blue, green, red = img[0, 0]
    if blue > red:  
        return "BGR"  
    elif red > blue:  
        return "RGB"  
    else:
        return "None"

def ImageArray2Cv2Image(image_array):
    bgr_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
    return bgr_image