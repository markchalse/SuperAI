

class EnvConfig:
    def __init__(self):
        self.camera_id = 0 #if start front camera, this camera_id=1
        
        #thread controler
        self.ai_online_flag = 'ai_super_online'
        self.server_online_flag = 'ai_singal_camera_top_online'
        self.server_activate_flag = 'ai_singal_camera_top_activate'