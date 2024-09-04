import sounddevice as sd  
import numpy as np  
import wave  
  
# 设置录音参数  
duration = 5  # 录音时长，单位秒  
fs = 44100  # 采样频率  
channels = 1  # 声道数，1为单声道，2为立体声  
  
# 初始化录音数组  
print("正在录音...")  
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)  
sd.wait()  # 等待录音完成  
  
# 将numpy数组保存到WAV文件  
print("录音完成，正在保存...")  
wav_output = wave.open('output.wav', 'wb')  
wav_output.setnchannels(channels)  
wav_output.setsampwidth(sd.int16(1).nbytes)  # 假设我们使用16位整数  
wav_output.setframerate(fs)  
wav_output.writeframes(myrecording.tobytes())  
wav_output.close()  
  
print("WAV文件已保存。")