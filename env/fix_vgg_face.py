import shutil
import os

#anaconda_base_path = r"D:\anaconda3_5_2\envs"
#anaconda_base_path = r"G:\workspace\majun\conda\envs"
#anaconda_base_path = r"C:\Users\1\.conda\envs"
#anaconda_base_path = r"F:\workspace\majun\conda\envs"
anaconda_base_path = r"G:\anaconda\envs"
env_name = "scene_learning_1"

env_path = os.path.join(anaconda_base_path,env_name)
vggface_lib_path = os.path.join(env_path,"Lib\site-packages\keras_vggface")

source_utils = os.path.join(vggface_lib_path,'utils.py')
bak_utils = os.path.join(vggface_lib_path,'utils.py.bak')
source_models = os.path.join(vggface_lib_path,'models.py')
bak_models = os.path.join(vggface_lib_path,'models.py.bak')

new_utils = r".\\keras_vggface_files\\utils.py"
new_models = r".\\keras_vggface_files\\models.py"

try:
    #shutil.copytree(source_utils, bak_utils)
    shutil.copy2(source_utils, bak_utils)
    shutil.copy2(source_models, bak_models)
    shutil.copy2(new_utils, source_utils)
    shutil.copy2(new_models, source_models)

except Exception as e:
    print(e)