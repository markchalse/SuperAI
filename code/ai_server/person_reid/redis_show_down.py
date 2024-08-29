import redis
import time

# 初始化Redis连接  
r = redis.Redis(host='localhost', port=6379, db=0) 


for i in range(3):
    r.set('ai_person_reid_show_down','1')
    time.sleep(0.3)