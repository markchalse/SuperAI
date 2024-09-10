import time
import os




def sound_file_names(path):
    names = []
    files = os.listdir(path)
    for file_name in files:
        if '.mp3' in file_name:
            names.append(file_name.split('.mp3')[0])
    return names
    




import pyttsx3
class PyTTS:
    def __init__(self,voice="zh",rate=150,volume=0.9):
        self.engine = pyttsx3.init()
        self.engine.setProperty('voice',voice)
        self.engine.setProperty('rate',rate)
        self.engine.setProperty('volume',volume)

    def text2voice_file(self,text,filename):
        

        #engine.say(text)
        #engine.runAndWait()

        self.engine.save_to_file(text,filename)
        self.engine.runAndWait()


import asyncio
import edge_tts
class EdgeTTS:
    def __init__(self,voice="zh-CN-XiaoxiaoNeural"):
        self.voice = voice
    
    
    def text2voice_file(self,text,filename):
        asyncio.run(self.amain(text,filename))
        
    async def amain(self,text,filename) -> None:
        for i in range(3):
            try:
                communicate = edge_tts.Communicate(text,self.voice)
                await communicate.save(filename)
                break
            except Exception as e:
                print (e)
                time.sleep(0.01) #延迟10ms
                print ("edge tts Try again !")
                
if __name__ == "__main___": 
    #et = EdgeTTS()               
    et = PyTTS()               
    #et.text2voice_file("你好，欢迎使用场景智慧学习平台，很高兴和你说话,你叫什么名字？",'test.mp3')
    et.text2voice_file("豫章故郡，洪都新府。星分翼轸，地接衡庐。襟三江而带五湖，控蛮荆而引瓯越。",'test.mp3')