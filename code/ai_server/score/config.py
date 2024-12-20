import os

class EnvConfig:
    def __init__(self):
        self.platform = "QT"#"QT"#"LAPTOP"#"QT"#"LAPTOP" # "QT"
        
        #login
        if self.platform == "LAPTOP":
            self.score_space = r"D:\ai_space\temp\score"
            
        elif self.platform == "QT":
            self.score_space = r"D:\ai_space\temp\score"
        
        
        
        #thread controler
        self.ai_online_flag = 'ai_super_online'
        self.server_online_flag = 'ai_score_online'
        self.server_activate_flag = 'ai_score_activate'
        
        
        #self.project_cfg_key = 'ai_project_cfg'
        self.project_cfg_key = '3'
        self.project_scores_key = 'ai_project_scores'
        
        
        
        self.platform_traj_result_key = 'ai_platform_trajectory_result'
        self.trajectory_id_key = 'ai_platform_trajectory_id'
        
        
        #redis tools
        self.MAX_LEN = 3
        
        
        
        self.square_goal_step_id = "1840309626334511106"
        self.triangular_goal_step_id = "1840309626334511107"