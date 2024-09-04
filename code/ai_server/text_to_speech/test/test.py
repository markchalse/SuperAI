#pip install pyttsx3 -i https://pypi.tuna.tsinghua.edu.cn/simple

'''
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('voice','zh')
engine.setProperty('rate',150)
engine.setProperty('volume',0.8)

text = "你好，欢迎使用场景智慧学习平台，请问有什么能够帮您的？"

engine.say(text)
engine.runAndWait()

engine.save_to_file(text,'output.wav')
engine.runAndWait()
'''



#pip install gTTS -i https://pypi.tuna.tsinghua.edu.cn/simple
'''
from gtts import gTTS
import os


# 定义文本到语音转换的函数
def text_to_speech(text, lang='zh-cn'): # 默认设置为中文语言
    # 使用gTTS创建语音对象，需要传入文本和语言代码
    tts = gTTS(text=text, lang=lang)
    # 定义保存语音文件的文件名，这里保存在当前目录下
    filename = 'speech.mp3'
    # 保存语音文件
    tts.save(filename)
    # 返回保存的文件名，以便后续使用
    return filename

# 示例文本，这里是一段中文文本
text = "大家好，我是一个程序员"
# 调用text_to_speech函数，将文本转换为语音，并指定使用中文
filename = text_to_speech(text, 'zh-cn')
# 打印出保存的文件路径，确认文件已经生成
print(f"Generated speech saved to {filename}")
os.system("start speech.mp3")
'''

#pip install edge-tts -i https://pypi.tuna.tsinghua.edu.cn/simple

import asyncio
import edge_tts

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
#from conf.Config import EnvConfig
import redis
import time


tts_voice = "zh-CN-XiaoxiaoNeural"
tts_mp3_file = 'test.mp3'
class EdgeSpeek:
    def __init__(self):
        #self.env = EnvConfig()
        #self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
        pass

    async def amain(self,text) -> None:
        #self.redis_client.set(self.env.tts_finish_siginal,'0')
        for i in range(3):
            try:
                """Main function"""
                communicate = edge_tts.Communicate(text,tts_voice)
                await communicate.save(tts_mp3_file)
                #self.redis_client.set(self.env.tts_finish_siginal,'1')
                break
            except Exception as e:
                print (e)
                time.sleep(0.01) #延迟10ms
                print ("edge tts Try again !")

if __name__ == "__main__":
    es = EdgeSpeek()
    asyncio.run(es.amain("很高兴和你说话,你叫什么名字？"))