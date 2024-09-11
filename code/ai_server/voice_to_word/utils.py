

import os
from config import EnvConfig

import base64

def add_asr_log(seq, path, word):
    if word=='':
        word='empty'
    env = EnvConfig()
    with open(env.ASR_LOG_PATH, 'a') as file:  
        word64 = base64.b64encode(word.encode('utf-8'))
        word64 = word64.decode('utf-8')  
        file.write(f"{seq} {path} {word64}\n")  

# 使用base64.b64decode进行解码  
# 注意：b64decode函数返回字节对象  
#decoded_bytes = base64.b64decode(encoded_str)  
# 如果原始数据是文本，将字节对象转换回字符串  
#decoded_str = decoded_bytes.decode('utf-8')

def read_asr_log(): 
    env = EnvConfig()
    if not os.path.exists(env.ASR_LOG_PATH): 
        return {}
    log_dict = {}  
    with open(env.ASR_LOG_PATH, 'r') as file:  
        for line in file:  
            try:
                parts = line.strip().split()  
                if len(parts) == 3:  
                    seq, path, word = parts  
                    log_dict[seq] = (path, word)
            except Exception as e:
                print (e)  
    return log_dict  

#res = read_asr_log()