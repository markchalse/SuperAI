import numpy as np 

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