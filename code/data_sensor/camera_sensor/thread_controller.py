import argparse
import time

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





def main(args):
    if args.func == 'offline':
        if args.env_serv!='':
            tc = ThreadControler(env=EnvConfig(server=args.env_serv))
        else:
            tc = ThreadControler()
        for i in range(3):
            tc.offline()
            time.sleep(0.3)
    if args.func == 'activate':
        if args.env_serv!='':
            tc = ThreadControler(env=EnvConfig(server=args.env_serv))
        else:
            tc = ThreadControler()
        for i in range(3):
            tc.activate()
            time.sleep(0.3)
    if args.func == 'deactivate':
        if args.env_serv!='':
            tc = ThreadControler(env=EnvConfig(server=args.env_serv))
        else:
            tc = ThreadControler()
        for i in range(3):
            tc.deactivate()
            time.sleep(0.3)
    if args.func == 'redis_set':
        if len(args.param)>0:
            print ('set readis: %s      value: %s'%(args.param[0],args.param[1]))
            tc = ThreadControler()
            for i in range(3):
                tc.redis_connect.set(args.param[0],args.param[1])
                time.sleep(0.3)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--func", type=str, help="function name|offline,activate,deactivate,redis_set") 
    parser.add_argument("--env_serv", type=str,default='', help="EnvConfig server name|feature_collect,person_reid") 
    parser.add_argument("--param", nargs='*' ,help="redis set|key value")
    args = parser.parse_args()  
    main(args)
