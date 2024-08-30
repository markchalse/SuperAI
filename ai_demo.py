# pip install pyqt5 -i https://pypi.tuna.tsinghua.edu.cn/simple
import sys  
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel , QHBoxLayout
from PyQt5.QtCore import Qt,QProcess  

BASE_PATH = r"F:\workspace\majun\zhiyuanchuang_space\ai_code\superai\SuperAI\code"

#-----------------------------------------------
CAMERA_SENSOR_PATH =  os.path.join(BASE_PATH,r"data_sensor\camera_sensor\script")
FACE_RECOGNITION_PATH = os.path.join(BASE_PATH,r"ai_server\face_recognition\script")
PERSON_REID_PATH = os.path.join(BASE_PATH,r"ai_server\person_reid\script")


class App(QWidget):  
    def __init__(self):  
        super().__init__()  
        self.initUI()  
        
        
        
  
    def initUI(self):  
        # 设置窗口  
        self.setWindowTitle('AI调试工具')  
        self.setGeometry(400, 400, 800, 400)  
  
        # 创建主垂直布局  
        mainLayout = QVBoxLayout()
        
        
        #------------------------------------------------------------------------- camera -------------------------------------------
        
        camera_layout = QHBoxLayout()
        
        # 按钮和状态灯  
        self.camera_buttons = []
        self.camera_show_buttons = []
        #self.camera_signals = []
        
        # 创建按钮  
        camera_start_btn = QPushButton(f'启动摄像头', self)
        camera_start_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        camera_start_btn.clicked.connect(lambda checked, path=os.path.join(CAMERA_SENSOR_PATH,'camera_sensor_start.bat') , server_name='camera' : self.execute_bat(path,server_name))
        
        camera_activate_btn = QPushButton(f'激活', self)
        camera_activate_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        camera_activate_btn.clicked.connect(lambda checked, path=os.path.join(CAMERA_SENSOR_PATH,'camera_sensor_activate.bat') , server_name='camera' : self.execute_bat(path,server_name))

        
        camera_deactive_btn = QPushButton(f'挂起', self)
        camera_deactive_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        camera_deactive_btn.clicked.connect(lambda checked, path=os.path.join(CAMERA_SENSOR_PATH,'camera_sensor_deactivate.bat') , server_name='camera' : self.execute_bat(path,server_name))

        
        camera_offline_btn = QPushButton(f'下线', self)
        camera_offline_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        camera_offline_btn.clicked.connect(lambda checked, path=os.path.join(CAMERA_SENSOR_PATH,'camera_sensor_down.bat') , server_name='camera' : self.execute_bat(path,server_name))

        
        camera_redis_show_btn = QPushButton(f'显示', self)
        camera_redis_show_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        camera_redis_show_btn.clicked.connect(lambda checked, path=os.path.join(CAMERA_SENSOR_PATH,'camera_redis_show.bat') , server_name='camera_show' : self.execute_bat(path,server_name))

        
        camera_redis_show_down_btn = QPushButton(f'关闭显示', self)
        camera_redis_show_down_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        camera_redis_show_down_btn.clicked.connect(lambda checked, path=os.path.join(CAMERA_SENSOR_PATH,'camera_redis_show_down.bat') , server_name='camera_show' : self.execute_bat(path,server_name))

        

        
        # 将按钮加入列表  
        self.camera_buttons.append(camera_start_btn) 
        self.camera_buttons.append(camera_activate_btn)  
        self.camera_buttons.append(camera_deactive_btn)  
        self.camera_buttons.append(camera_offline_btn)  
        
        self.camera_show_buttons.append(camera_redis_show_btn)
        self.camera_show_buttons.append(camera_redis_show_down_btn)
        
        # 添加到布局
        camera_layout.addWidget(camera_start_btn)
        camera_layout.addWidget(camera_activate_btn)
        camera_layout.addWidget(camera_deactive_btn)
        camera_layout.addWidget(camera_offline_btn)
        camera_layout.addWidget(camera_redis_show_btn)
        camera_layout.addWidget(camera_redis_show_down_btn)
        
        
        camera_label = QLabel('摄像头服务', self)
        
        camera_container = QWidget(self)  
        camera_container.setLayout(camera_layout)
        

        
        #------------------------------------------------------------------------- face recognition -------------------------------------------
        
        
        face_layout = QHBoxLayout()
        
        # 按钮和状态灯  
        self.face_buttons = []
        self.face_show_buttons = []
        
        # 创建按钮  
        face_start_btn = QPushButton(f'启动人脸识别', self)
        face_start_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        face_start_btn.clicked.connect(lambda checked, path=os.path.join(FACE_RECOGNITION_PATH,'face_recognition_start.bat') , server_name='face' : self.execute_bat(path,server_name))
        
        face_activate_btn = QPushButton(f'激活', self)
        face_activate_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        face_activate_btn.clicked.connect(lambda checked, path=os.path.join(FACE_RECOGNITION_PATH,'face_recognition_activate.bat') , server_name='face' : self.execute_bat(path,server_name))

        
        face_deactive_btn = QPushButton(f'挂起', self)
        face_deactive_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        face_deactive_btn.clicked.connect(lambda checked, path=os.path.join(FACE_RECOGNITION_PATH,'face_recognition_deactivate.bat') , server_name='face' : self.execute_bat(path,server_name))

        
        face_offline_btn = QPushButton(f'下线', self)
        face_offline_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        face_offline_btn.clicked.connect(lambda checked, path=os.path.join(FACE_RECOGNITION_PATH,'face_recognition_down.bat') , server_name='face' : self.execute_bat(path,server_name))

        
        face_redis_show_btn = QPushButton(f'显示', self)
        face_redis_show_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        face_redis_show_btn.clicked.connect(lambda checked, path=os.path.join(FACE_RECOGNITION_PATH,'face_recognition_redis_show.bat') , server_name='face_show' : self.execute_bat(path,server_name))

        
        face_redis_show_down_btn = QPushButton(f'关闭显示', self)
        face_redis_show_down_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        face_redis_show_down_btn.clicked.connect(lambda checked, path=os.path.join(FACE_RECOGNITION_PATH,'face_recognition_redis_show_down.bat') , server_name='face_show' : self.execute_bat(path,server_name))

        

        
        # 将按钮加入列表  
        self.face_buttons.append(face_start_btn) 
        self.face_buttons.append(face_activate_btn)  
        self.face_buttons.append(face_deactive_btn)  
        self.face_buttons.append(face_offline_btn)  
        
        self.face_show_buttons.append(face_redis_show_btn)
        self.face_show_buttons.append(face_redis_show_down_btn)
        
        # 添加到布局
        face_layout.addWidget(face_start_btn)
        face_layout.addWidget(face_activate_btn)
        face_layout.addWidget(face_deactive_btn)
        face_layout.addWidget(face_offline_btn)
        face_layout.addWidget(face_redis_show_btn)
        face_layout.addWidget(face_redis_show_down_btn)
        
        
        face_label = QLabel('人脸识别服务', self)
        
        face_container = QWidget(self)  
        face_container.setLayout(face_layout)
        

        #------------------------------------------------------------------------- person ReID feature collect -------------------------------------------
        
        
        feature_collect_layout = QHBoxLayout()
        
        # 按钮和状态灯  
        self.feature_collect_buttons = []
        #self.reid_show_buttons = []
        
        # 创建按钮  
        feature_collect_start_btn = QPushButton(f'启动构建特征', self)
        feature_collect_start_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        feature_collect_start_btn.clicked.connect(lambda checked, path=os.path.join(PERSON_REID_PATH,'feature_collect_start.bat') , server_name='feature_collect' : self.execute_bat(path,server_name))
        
        feature_collect_activate_btn = QPushButton(f'激活', self)
        feature_collect_activate_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        feature_collect_activate_btn.clicked.connect(lambda checked, path=os.path.join(PERSON_REID_PATH,'feature_collect_activate.bat') , server_name='feature_collect' : self.execute_bat(path,server_name))

        
        feature_collect_deactive_btn = QPushButton(f'挂起', self)
        feature_collect_deactive_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        feature_collect_deactive_btn.clicked.connect(lambda checked, path=os.path.join(PERSON_REID_PATH,'feature_collect_deactive.bat') , server_name='feature_collect' : self.execute_bat(path,server_name))

        
        feature_collect_offline_btn = QPushButton(f'下线', self)
        feature_collect_offline_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        feature_collect_offline_btn.clicked.connect(lambda checked, path=os.path.join(PERSON_REID_PATH,'feature_collect_down.bat') , server_name='feature_collect' : self.execute_bat(path,server_name))

        
        feature_collect_redis_show_btn = QPushButton(f'', self)
        feature_collect_redis_show_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        #reid_redis_show_btn.clicked.connect(lambda checked, path=os.path.join(PERSON_REID_PATH,'person_reid_redis_show.bat') , server_name='reid_show' : self.execute_bat(path,server_name))

        
        feature_collect_redis_show_down_btn = QPushButton(f'', self)
        feature_collect_redis_show_down_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        #reid_redis_show_down_btn.clicked.connect(lambda checked, path=os.path.join(PERSON_REID_PATH,'person_reid_redis_show_down.bat') , server_name='reid_show' : self.execute_bat(path,server_name))

        

        
        # 将按钮加入列表  
        self.feature_collect_buttons.append(feature_collect_start_btn) 
        self.feature_collect_buttons.append(feature_collect_activate_btn)  
        self.feature_collect_buttons.append(feature_collect_deactive_btn)  
        self.feature_collect_buttons.append(feature_collect_offline_btn)  
        
        #self.reid_show_buttons.append(reid_redis_show_btn)
        #self.reid_show_buttons.append(reid_redis_show_down_btn)
        
        # 添加到布局
        feature_collect_layout.addWidget(feature_collect_start_btn)
        feature_collect_layout.addWidget(feature_collect_activate_btn)
        feature_collect_layout.addWidget(feature_collect_deactive_btn)
        feature_collect_layout.addWidget(feature_collect_offline_btn)
        feature_collect_layout.addWidget(feature_collect_redis_show_btn)
        feature_collect_layout.addWidget(feature_collect_redis_show_down_btn)
        
        
        feature_collect_label = QLabel('行人重识别特征构建服务', self)
        
        feature_collect_container = QWidget(self)  
        feature_collect_container.setLayout(feature_collect_layout)
        
        
        
        
        
        
        #------------------------------------------------------------------------- person ReID -------------------------------------------
        
        
        reid_layout = QHBoxLayout()
        
        # 按钮和状态灯  
        self.reid_buttons = []
        self.reid_show_buttons = []
        
        # 创建按钮  
        reid_start_btn = QPushButton(f'启动行人重识别', self)
        reid_start_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        reid_start_btn.clicked.connect(lambda checked, path=os.path.join(PERSON_REID_PATH,'person_reid_start.bat') , server_name='reid' : self.execute_bat(path,server_name))
        
        reid_activate_btn = QPushButton(f'激活', self)
        reid_activate_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        reid_activate_btn.clicked.connect(lambda checked, path=os.path.join(PERSON_REID_PATH,'person_reid_activate.bat') , server_name='reid' : self.execute_bat(path,server_name))

        
        reid_deactive_btn = QPushButton(f'挂起', self)
        reid_deactive_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        reid_deactive_btn.clicked.connect(lambda checked, path=os.path.join(PERSON_REID_PATH,'person_reid_deactivate.bat') , server_name='reid' : self.execute_bat(path,server_name))

        
        reid_offline_btn = QPushButton(f'下线', self)
        reid_offline_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        reid_offline_btn.clicked.connect(lambda checked, path=os.path.join(PERSON_REID_PATH,'person_reid_down.bat') , server_name='reid' : self.execute_bat(path,server_name))

        
        reid_redis_show_btn = QPushButton(f'显示', self)
        reid_redis_show_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        reid_redis_show_btn.clicked.connect(lambda checked, path=os.path.join(PERSON_REID_PATH,'person_reid_redis_show.bat') , server_name='reid_show' : self.execute_bat(path,server_name))

        
        reid_redis_show_down_btn = QPushButton(f'关闭显示', self)
        reid_redis_show_down_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        reid_redis_show_down_btn.clicked.connect(lambda checked, path=os.path.join(PERSON_REID_PATH,'person_reid_redis_show_down.bat') , server_name='reid_show' : self.execute_bat(path,server_name))

        

        
        # 将按钮加入列表  
        self.reid_buttons.append(reid_start_btn) 
        self.reid_buttons.append(reid_activate_btn)  
        self.reid_buttons.append(reid_deactive_btn)  
        self.reid_buttons.append(reid_offline_btn)  
        
        self.reid_show_buttons.append(reid_redis_show_btn)
        self.reid_show_buttons.append(reid_redis_show_down_btn)
        
        # 添加到布局
        reid_layout.addWidget(reid_start_btn)
        reid_layout.addWidget(reid_activate_btn)
        reid_layout.addWidget(reid_deactive_btn)
        reid_layout.addWidget(reid_offline_btn)
        reid_layout.addWidget(reid_redis_show_btn)
        reid_layout.addWidget(reid_redis_show_down_btn)
        
        
        reid_label = QLabel('行人重识别服务', self)
        
        reid_container = QWidget(self)  
        reid_container.setLayout(reid_layout)
        
        
        
        
        
        
        
        
        
        
        split_label1 = QLabel('----------------------------------------------------', self)
        split_label2 = QLabel('----------------------------------------------------', self)
        split_label3 = QLabel('----------------------------------------------------', self)
        # 将包含子布局的QWidget添加到主布局中  
        mainLayout.addWidget(camera_label)
        mainLayout.addWidget(camera_container)
        mainLayout.addWidget(split_label1)
        
        mainLayout.addWidget(face_label)
        mainLayout.addWidget(face_container)
        mainLayout.addWidget(split_label2)
        
        mainLayout.addWidget(feature_collect_label)
        mainLayout.addWidget(feature_collect_container)
        mainLayout.addWidget(split_label3)
        
        mainLayout.addWidget(reid_label)
        mainLayout.addWidget(reid_container)
        
        
        # 创建一个QLabel并添加到主布局中  
        #label = QLabel('这是一个标签', self)  
        #mainLayout.addWidget(label)  
  
         
        # 设置窗口的主布局  
        self.setLayout(mainLayout) 
  
    def execute_bat(self, path , server_name):
        if server_name == 'camera':
            buttons = self.camera_buttons
        if server_name == 'camera_show':
            buttons = self.camera_show_buttons   
        if server_name == 'face':
            buttons = self.face_buttons
        if server_name == 'face_show':
            buttons = self.face_show_buttons 
        if server_name == 'feature_collect':
            buttons = self.feature_collect_buttons
        if server_name == 'reid':
            buttons = self.reid_buttons
        if server_name == 'reid_show':
            buttons = self.reid_show_buttons
        # 执行BAT文件  
        process = QProcess(self)  
        process.start(path)  
        
        for button in buttons:
            button.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255,255,255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        
        buttons[buttons.index(self.sender())].setStyleSheet("QPushButton {"
                                  "  background-color: rgb(135,206,235);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
  
if __name__ == '__main__':  
    app = QApplication(sys.argv)  
    ex = App()  
    ex.show()  
    sys.exit(app.exec_())