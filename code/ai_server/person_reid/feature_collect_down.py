import time
from config import EnvConfig
from thread_controller import ThreadControler

tc = ThreadControler(EnvConfig(server='feature_collect'))
for i in range(3):
    tc.offline()
    time.sleep(0.3)
    