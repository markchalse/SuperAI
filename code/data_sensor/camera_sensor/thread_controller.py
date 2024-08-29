
import redis
from config import EnvConfig


class ThreadControler:
    def __init__(self,env=EnvConfig()):
        self.env= env
        self.redis_connect = redis.Redis(host='localhost', port=6379, db=0)
        
    def init_thread(self):
        self.redis_connect.set(self.env.server_online_flag,'1')
        self.redis_connect.set(self.env.server_activate_flag,'0')
    
    def online(self):
        self.redis_connect.set(self.env.server_online_flag,'1')
    
    def offline(self):
        self.redis_connect.set(self.env.server_online_flag,'0')
    
    def ai_online(self):
        self.redis_connect.set(self.env.ai_online_flag,'1')
            
    def ai_offline(self):
        self.redis_connect.set(self.env.ai_online_flag,'0')
        
    def activate(self):
        self.redis_connect.set(self.env.server_activate_flag,'1')
        
    def deactivate(self):
        self.redis_connect.set(self.env.server_activate_flag,'0')
        
    def check_activate(self):
        return self.redis_connect.get(self.env.server_activate_flag)==b'1'
        
    def check_on_line(self):
        return self.redis_connect.get(self.env.server_online_flag)==b'1'
    
    def check_ai_online(self):
        return self.redis_connect.get(self.env.ai_online_flag)==b'1'
    