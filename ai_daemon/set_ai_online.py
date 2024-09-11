
import time
import redis
from config import EnvConfig

env= EnvConfig()
r = redis.Redis(host='localhost', port=6379, db=0)  
for i in range(3):
    r.set(env.ai_online_flag, '1')
    time.sleep(0.3)