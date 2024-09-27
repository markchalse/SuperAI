import os

class EnvConfig:
    def __init__(self):
        self.platform = "LAPTOP"#"QT"#"LAPTOP"#"QT"#"LAPTOP" # "QT"
        
        #login
        if self.platform == "LAPTOP":
            self.score_space = r"F:\majun\tmp\score"
            
        elif self.platform == "QT":
            self.score_space = r"G:\workspace\majun\temp\score"
        
        
        
        #thread controler
        self.ai_online_flag = 'ai_super_online'
        self.server_online_flag = 'ai_score_online'
        self.server_activate_flag = 'ai_score_activate'
        
        
        self.project_cfg_key = 'ai_project_cfg'
        self.project_scores_key = 'ai_project_scores'
        
        
        
        self.platform_traj_result_key = 'ai_platform_trajectory_result'
        
        
        #redis tools
        self.MAX_LEN = 3
        
        