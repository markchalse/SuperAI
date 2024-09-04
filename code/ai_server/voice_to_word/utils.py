

import os

def add_asr_log(seq, path, word): 
    with open('ASR.LOG', 'a') as file:  
        file.write(f"{seq} {path} {word}\n")  
  
def read_asr_log(): 
    if not os.path.exists('ASR.LOG'):  
        return {}
    log_dict = {}  
    with open('ASR.LOG', 'r') as file:  
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