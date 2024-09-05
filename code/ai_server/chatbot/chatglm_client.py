from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import Optional
import base64
import requests
app = FastAPI()



# 假设您已经编写好了一个处理图片的函数
# def process_images(image1: UploadFile, image2: UploadFile) -> str:
#     # 这里是图片处理逻辑
#     # 举例：返回两张图片的base64编码拼接的字符串
#     image1_data = image1.file.read()
#     image2_data = image2.file.read()
#     return base64.b64encode(image1_data).decode('utf-8') + base64.b64encode(image2_data).decode('utf-8')
#
# @app.post("/upload")
# async def upload_images(image1: UploadFile = File(...), image2: UploadFile = File(...)):
#     try:
#         if image1 and image2:
#             processed_text = process_images(image1, image2)
#             return {"result": processed_text}
#         else:
#             raise HTTPException(status_code=400, detail="Please upload two images")
#     except Exception as e:
#         return {"error": str(e)}
#
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


import requests
import json

# 服务端的URL
#url = 'http://localhost:5000/chat'
url = 'http://192.168.161.241:5000/chat'

import requests
import json

# 服务器的URL


# 准备发送的数据
data = {
    'user_input': "什么是大语言模型"
}
headers = {
    'Content-Type': 'application/json'
}

response = requests.post(url, data=json.dumps(data), headers=headers)
# 发送POST请求
#response = requests.post(url, json=data)

# 检查响应状态码
if response.status_code == 200:
    # 打印返回的答案
    answer = response.json().get('response')
    print(answer)
else:
    # 打印错误信息
    print(f'Error: {response.status_code}, {response.text}')

    result_dict = json.loads(response.text)
    print (result_dict)
    print (result_dict['response'])
    #print (response.text.encode('utf-8'))

quit()
def send_question(question):
    # 构建请求数据
    #data = {'user_input': question}

    # 发送POST请求
    response = requests.post(URL, json=question)
    print(response.json())

    # 检查响应状态码
    if response.status_code == 200:
        # 打印服务端返回的响应
        print('服务端回复:', response.json()['response'])
    else:
        # 打印错误信息
        print('发生错误:', response.status_code)


if __name__ == '__main__':
    # 提问内容
    question = "什么是大语言模型"


    # 打印返回的结果

    # 发送问题到服务端
    send_question(question)

# import requests
# import json
#
# try:
#     response = requests.get('http://localhost:5000/chat')
#     response.raise_for_status()  # 检查是否请求成功
#     data = response.json()  # 尝试解析 JSON
# except requests.exceptions.HTTPError as http_err:
#     print(f"HTTP error occurred: {http_err}")
# except requests.exceptions.JSONDecodeError as json_err:
#     print(f"JSON decode error occurred: {json_err}")
#     # 处理非 JSON 数据或其他逻辑
# except requests.exceptions.RequestException as err:
#     print(f"Request error occurred: {err}")