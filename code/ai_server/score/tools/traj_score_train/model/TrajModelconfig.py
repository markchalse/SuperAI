class EnvConfig():
    def __init__(self):
        platform = 'LAPTOP'#'QT'#'LAPTOP'
        
        
        if platform == 'LAPTOP':
            self.train_base_path = r'F:\majun\img\traj_img\train'
            self.model_save_path= r'F:\majun\img\traj_img'
            self.test_base_path = r'F:\majun\img\traj_img\eval2'
        elif platform == 'QT':
            self.train_base_path = r'F:\majun\img\traj_img'
            self.model_save_path= r'G:\workspace\majun\models\super_ai\trajectory_score'
        self.batch_size = 500
        self.learning_rate = 0.001
        self.epoch = 5