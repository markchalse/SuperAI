import psutil  
import os

#import subprocess  
  
# 启动一个子进程  
#p = subprocess.Popen(["some_command"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)  
  
#pid = p.pid  

pid = 16000  
try:
    # 使用psutil检查PID  
    process = psutil.Process(pid)  
    if process.is_running():  
        print(f"PID {pid} is still running.")  
    else:  
        print(f"PID {pid} is not running.")  
except Exception as e:
    print(e)    
    if 'not found' in str(e):
        print ('haha')
        bat_path= r'F:\workspace\majun\zhiyuanchuang_space\ai_code\superai\SuperAI\code\data_sensor\camera_sensor\script\camera_redis_show.bat'
        os.system('start '+bat_path)
# 记得在脚本结束时清理子进程  
#p.terminate()  # 发送SIGTERM信号  
#p.wait()  # 等待进程结束