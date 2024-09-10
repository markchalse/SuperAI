from config import EnvConfig
import os
import time
if __name__=="__main__":
    env = EnvConfig()
    lock_file = env.codebase_path+r"\ai_daemon\tmp.lock"
    print(lock_file)
    if os.path.exists(lock_file):
        os.remove(lock_file)
        print ('refresh the lock file!')
        time.sleep(2)