import time
from config import EnvConfig
from thread_controller import ThreadControler

tc = ThreadControler(EnvConfig(server='feature_collect'))
for i in range(3):
    tc.deactivate()
    time.sleep(0.3)
    