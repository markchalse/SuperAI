

import os
from config import EnvConfig

import base64

def add_chatbot_log(seq, ask, answer):
    env = EnvConfig()
    with open(env.chatbot_log_path, 'a') as file:  
        #file.write(f"{seq} {ask} {answer}\n")  
        answer64 = base64.b64encode(answer.encode('utf-8'))
        answer64 = answer64.decode('utf-8')  
        file.write(f"{seq} {ask} {answer64}\n")  

# 使用base64.b64decode进行解码  
# 注意：b64decode函数返回字节对象  
#decoded_bytes = base64.b64decode(encoded_str)  
# 如果原始数据是文本，将字节对象转换回字符串  
#decoded_str = decoded_bytes.decode('utf-8') 

def read_chatbot_log(): 
    env = EnvConfig()
    if not os.path.exists(env.chatbot_log_path): 
        return {}
    log_dict = {}  
    with open(env.chatbot_log_path, 'r') as file:  
        for line in file:  
            try:
                parts = line.strip().split()  
                #print (parts)
                if len(parts) == 3:  
                    seq, ask, answer = parts  
                    log_dict[seq] = (ask, answer)
            except Exception as e:
                print (e)  
    return log_dict  


#from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import Optional
import base64
import requests
import json
class GLM:
    def __init__(self):
        self.env = EnvConfig()
        self.url = self.env.server_url
    
    def get_response(self,ask_str):
        # 准备发送的数据
        data = {'user_input': ask_str}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.url, data=json.dumps(data), headers=headers)
        try:
            # 检查响应状态码
            if response.status_code == 200:
                # 打印返回的答案
                answer = response.json().get('response')
                print ('code:200')
                print(answer)
                return answer
            else:
                # 打印错误信息
                #print(f'Error: {response.status_code}, {response.text}')
                print (f'code:{response.status_code}')
                result_dict = json.loads(response.text)
                #print (result_dict)
                print (result_dict['response'])
                return result_dict['response']
        except Exception as e:
            print (e)
            return e


class BaiduAI:
    def __init__(self):
        self.API_KEY = "idQrZUZVc5RctuQyHdgykfMn"
        self.SECRET_KEY = "EvsMQlswet0GWQm9GkTcghb3Wki9fna4"
        self.max_output_tokens = 50
        self.access_token = self.get_access_token()

    def get_access_token(self):
        """
        使用 AK，SK 生成鉴权签名（Access Token）
        :return: access_token，或是None(如果错误)
        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": self.API_KEY, "client_secret": self.SECRET_KEY}
        return str(requests.post(url, params=params).json().get("access_token"))
    

    def get_response(self,question):
        #url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie_speed?access_token=" + get_access_token()
        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie_speed?access_token=" + self.access_token
        payload = json.dumps({
            "max_output_tokens":self.max_output_tokens,
            "messages": [
                {
                    "role": "user",
                    #"content": "您好"
                    "content": question
                },
                #{
                #    "role": "assistant",
                #    "content": "您好！有什么我可以帮助您的吗？请随时告诉我，我会尽力提供帮助。"
                #}
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            json_string = response.text
            #print(json_string)
            result_dict = json.loads(json_string)
            print (result_dict['result'])
            return result_dict['result']
        except Exception as e:
            print (e)
            return e
    



if __name__ == '__main__':   
    #cb = ChatBot()
    #res = cb.get_response('向我介绍一下你自己')
    #res = cb.get_response('你了解工科教育吗')
    #res = cb.get_response('你了解千分尺吗')
    #print (res)
    
    
    #bd = BaiduAI()
    #print(bd.get_response('你了解千分尺吗'))
    
    log_dict = read_chatbot_log()
    print (log_dict.keys())
    