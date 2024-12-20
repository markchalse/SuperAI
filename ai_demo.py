# pip install pyqt5 -i https://pypi.tuna.tsinghua.edu.cn/simple
import sys  
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel , QHBoxLayout, QTextEdit,  QScrollArea 
from PyQt5.QtCore import Qt,QProcess  
import redis
import json
import time
import datetime

BASE_PATH = r"D:\ai_space\code\superai"


#-----------------------------------------------
CAMERA_SENSOR_PATH =  os.path.join(BASE_PATH,r"code\data_sensor\camera_sensor\script")
CAMERA_SENSOR_TOP_PATH =  os.path.join(BASE_PATH,r"code\data_sensor\camera_sensor_top\script")
FACE_RECOGNITION_PATH = os.path.join(BASE_PATH,r"code\ai_server\face_recognition\script")
PERSON_REID_PATH = os.path.join(BASE_PATH,r"code\ai_server\person_reid\script")
TTS_PATH = os.path.join(BASE_PATH,r"code\ai_server\text_to_speech\script")
ASR_PATH = os.path.join(BASE_PATH,r"code\ai_server\voice_to_word\script")
CHATBOT_PATH = os.path.join(BASE_PATH,r"code\ai_server\chatbot\script")
DAEMON_PATH = os.path.join(BASE_PATH,r"ai_daemon\script")
SCORE_PATH = os.path.join(BASE_PATH,r"code\ai_server\score\script")
SMDPR_PATH = os.path.join(BASE_PATH,r"code\ai_server\servo_motor_drive_platform_recognition\script")
SMDPJ_PATH = os.path.join(BASE_PATH,r"code\ai_server\platform_trajectory\script")


class App(QWidget):  
    def __init__(self):  
        super().__init__()  
        self.initUI()  
        
        
        
  
    def initUI(self):  
        # 设置窗口  
        self.setWindowTitle('AI调试工具')  
        self.setGeometry(400, 400, 1200, 1500)  
  
        # 创建主垂直布局  
        mainLayout = QVBoxLayout()
        
        
        #------------------------------------------------------------------------- camera -------------------------------------------
        
        camera_layout = QHBoxLayout()
        
        # 按钮和状态灯  
        self.camera_buttons = []
        self.camera_show_buttons = []
        #self.camera_signals = []
        
        # 创建按钮  
        camera_start_btn = QPushButton(f'启动前摄像头', self)
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
        
        
        camera_label = QLabel('前摄像头服务', self)
        
        camera_container = QWidget(self)  
        camera_container.setLayout(camera_layout)
        
        #------------------------------------------------------------------------- camera top -------------------------------------------
        
        camera_top_layout = QHBoxLayout()
        
        # 按钮和状态灯  
        self.camera_top_buttons = []
        self.camera_top_show_buttons = []
        #self.camera_signals = []
        
        # 创建按钮  
        camera_top_start_btn = QPushButton(f'启动顶摄像头', self)
        camera_top_start_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        camera_top_start_btn.clicked.connect(lambda checked, path=os.path.join(CAMERA_SENSOR_TOP_PATH,'camera_sensor_start.bat') , server_name='camera_top' : self.execute_bat(path,server_name))
        
        camera_top_activate_btn = QPushButton(f'激活', self)
        camera_top_activate_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        camera_top_activate_btn.clicked.connect(lambda checked, path=os.path.join(CAMERA_SENSOR_TOP_PATH,'camera_sensor_activate.bat') , server_name='camera_top' : self.execute_bat(path,server_name))

        
        camera_top_deactive_btn = QPushButton(f'挂起', self)
        camera_top_deactive_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        camera_top_deactive_btn.clicked.connect(lambda checked, path=os.path.join(CAMERA_SENSOR_TOP_PATH,'camera_sensor_deactivate.bat') , server_name='camera_top' : self.execute_bat(path,server_name))

        
        camera_top_offline_btn = QPushButton(f'下线', self)
        camera_top_offline_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        camera_top_offline_btn.clicked.connect(lambda checked, path=os.path.join(CAMERA_SENSOR_TOP_PATH,'camera_sensor_down.bat') , server_name='camera_top' : self.execute_bat(path,server_name))

        
        camera_top_redis_show_btn = QPushButton(f'显示', self)
        camera_top_redis_show_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        camera_top_redis_show_btn.clicked.connect(lambda checked, path=os.path.join(CAMERA_SENSOR_TOP_PATH,'camera_redis_show.bat') , server_name='camera_top_show' : self.execute_bat(path,server_name))

        
        camera_top_redis_show_down_btn = QPushButton(f'关闭显示', self)
        camera_top_redis_show_down_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        camera_top_redis_show_down_btn.clicked.connect(lambda checked, path=os.path.join(CAMERA_SENSOR_TOP_PATH,'camera_redis_show_down.bat') , server_name='camera_top_show' : self.execute_bat(path,server_name))

        

        
        # 将按钮加入列表  
        self.camera_top_buttons.append(camera_top_start_btn) 
        self.camera_top_buttons.append(camera_top_activate_btn)  
        self.camera_top_buttons.append(camera_top_deactive_btn)  
        self.camera_top_buttons.append(camera_top_offline_btn)  
        
        self.camera_top_show_buttons.append(camera_top_redis_show_btn)
        self.camera_top_show_buttons.append(camera_top_redis_show_down_btn)
        
        # 添加到布局
        camera_top_layout.addWidget(camera_top_start_btn)
        camera_top_layout.addWidget(camera_top_activate_btn)
        camera_top_layout.addWidget(camera_top_deactive_btn)
        camera_top_layout.addWidget(camera_top_offline_btn)
        camera_top_layout.addWidget(camera_top_redis_show_btn)
        camera_top_layout.addWidget(camera_top_redis_show_down_btn)
        
        
        camera_top_label = QLabel('顶摄像头服务', self)
        
        camera_top_container = QWidget(self)  
        camera_top_container.setLayout(camera_top_layout)
        
        
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
        
        
        
        
        
        #------------------------------------------------------------------------- text to sound TTS -------------------------------------------
        
        
        tts_layout = QHBoxLayout()
        
        # 按钮和状态灯  
        self.tts_buttons = []
        self.tts_show_buttons = []
        
        # 创建按钮  
        tts_start_btn = QPushButton(f'启动文字转音频', self)
        tts_start_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        tts_start_btn.clicked.connect(lambda checked, path=os.path.join(TTS_PATH,'tts_start.bat') , server_name='tts' : self.execute_bat(path,server_name))
        
        tts_activate_btn = QPushButton(f'激活', self)
        tts_activate_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        tts_activate_btn.clicked.connect(lambda checked, path=os.path.join(TTS_PATH,'tts_activate.bat') , server_name='tts' : self.execute_bat(path,server_name))

        
        tts_deactive_btn = QPushButton(f'挂起', self)
        tts_deactive_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        tts_deactive_btn.clicked.connect(lambda checked, path=os.path.join(TTS_PATH,'tts_deactivate.bat') , server_name='tts' : self.execute_bat(path,server_name))

        
        tts_offline_btn = QPushButton(f'下线', self)
        tts_offline_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        tts_offline_btn.clicked.connect(lambda checked, path=os.path.join(TTS_PATH,'tts_down.bat') , server_name='tts' : self.execute_bat(path,server_name))

        
        tts_redis_show_btn = QPushButton(f'显示音频文字', self)
        tts_redis_show_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        tts_redis_show_btn.clicked.connect(lambda checked, path='tts_text' , server_name='tts_show' : self.execute_bat(path,server_name))

        
        tts_redis_show_down_btn = QPushButton(f'显示音频文件', self)
        tts_redis_show_down_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        tts_redis_show_down_btn.clicked.connect(lambda checked, path='tts_sound' , server_name='tts_show' : self.execute_bat(path,server_name))


        tts_text_send_btn = QPushButton(f'发送文字', self)
        tts_text_send_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        tts_text_send_btn.clicked.connect(lambda checked, path='tts_sound' , server_name='tts_send' : self.execute_bat(path,server_name))

        
        # 将按钮加入列表  
        self.tts_buttons.append(tts_start_btn) 
        self.tts_buttons.append(tts_activate_btn)  
        self.tts_buttons.append(tts_deactive_btn)  
        self.tts_buttons.append(tts_offline_btn)  
        
        self.tts_show_buttons.append(tts_redis_show_btn)
        self.tts_show_buttons.append(tts_redis_show_down_btn)
        
        # 添加到布局
        tts_layout.addWidget(tts_start_btn)
        tts_layout.addWidget(tts_activate_btn)
        tts_layout.addWidget(tts_deactive_btn)
        tts_layout.addWidget(tts_offline_btn)
        tts_layout.addWidget(tts_redis_show_btn)
        tts_layout.addWidget(tts_redis_show_down_btn)
        
        
        tts_label = QLabel('文字转音频服务', self)        
        # 或者创建一个可以多行显示的 QTextEdit
        self.tts_text_edit = QTextEdit(self)

        self.tts_text_send_edit = QTextEdit(self)

        tts_container = QWidget(self)  
        tts_container.setLayout(tts_layout)
        
        
        
        
        #------------------------------------------------------------------------- voice to word ASR -------------------------------------------
        
        
        asr_layout = QHBoxLayout()
        
        # 按钮和状态灯  
        self.asr_buttons = []
        self.asr_show_buttons = []
        
        # 创建按钮  
        asr_start_btn = QPushButton(f'启动音频识别', self)
        asr_start_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        asr_start_btn.clicked.connect(lambda checked, path=os.path.join(ASR_PATH,'asr_start.bat') , server_name='asr' : self.execute_bat(path,server_name))
        
        asr_activate_btn = QPushButton(f'激活', self)
        asr_activate_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        asr_activate_btn.clicked.connect(lambda checked, path=os.path.join(ASR_PATH,'asr_activate.bat') , server_name='asr' : self.execute_bat(path,server_name))

        
        asr_deactive_btn = QPushButton(f'挂起', self)
        asr_deactive_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        asr_deactive_btn.clicked.connect(lambda checked, path=os.path.join(ASR_PATH,'asr_deactivate.bat') , server_name='asr' : self.execute_bat(path,server_name))

        
        asr_offline_btn = QPushButton(f'下线', self)
        asr_offline_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        asr_offline_btn.clicked.connect(lambda checked, path=os.path.join(ASR_PATH,'asr_down.bat') , server_name='asr' : self.execute_bat(path,server_name))

        
        asr_redis_show_btn = QPushButton(f'显示音频请求', self)
        asr_redis_show_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        asr_redis_show_btn.clicked.connect(lambda checked, path='asr_sound' , server_name='asr_show' : self.execute_bat(path,server_name))

        
        asr_redis_show_down_btn = QPushButton(f'显示音频识别', self)
        asr_redis_show_down_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        asr_redis_show_down_btn.clicked.connect(lambda checked, path='asr_text' , server_name='asr_show' : self.execute_bat(path,server_name))


        asr_text_send_btn = QPushButton(f'发送路径', self)
        asr_text_send_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        asr_text_send_btn.clicked.connect(lambda checked, path='asr_sound' , server_name='asr_send' : self.execute_bat(path,server_name))

        
        # 将按钮加入列表  
        self.asr_buttons.append(asr_start_btn) 
        self.asr_buttons.append(asr_activate_btn)  
        self.asr_buttons.append(asr_deactive_btn)  
        self.asr_buttons.append(asr_offline_btn)  
        
        self.asr_show_buttons.append(asr_redis_show_btn)
        self.asr_show_buttons.append(asr_redis_show_down_btn)
        
        # 添加到布局
        asr_layout.addWidget(asr_start_btn)
        asr_layout.addWidget(asr_activate_btn)
        asr_layout.addWidget(asr_deactive_btn)
        asr_layout.addWidget(asr_offline_btn)
        asr_layout.addWidget(asr_redis_show_btn)
        asr_layout.addWidget(asr_redis_show_down_btn)
        
        
        asr_label = QLabel('音频转文字服务', self)        
        # 或者创建一个可以多行显示的 QTextEdit
        self.asr_text_edit = QTextEdit(self)

        self.asr_text_send_edit = QTextEdit(self)

        asr_container = QWidget(self)  
        asr_container.setLayout(asr_layout)
        
        
        #------------------------------------------------------------------------- chatbot -------------------------------------------
        
        
        chatbot_layout = QHBoxLayout()
        
        # 按钮和状态灯  
        self.chatbot_buttons = []
        self.chatbot_show_buttons = []
        
        # 创建按钮  
        chatbot_start_btn = QPushButton(f'启动大语言对话', self)
        chatbot_start_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        chatbot_start_btn.clicked.connect(lambda checked, path=os.path.join(CHATBOT_PATH,'chatbot_start.bat') , server_name='chatbot' : self.execute_bat(path,server_name))
        
        chatbot_activate_btn = QPushButton(f'激活', self)
        chatbot_activate_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        chatbot_activate_btn.clicked.connect(lambda checked, path=os.path.join(CHATBOT_PATH,'chatbot_activate.bat') , server_name='chatbot' : self.execute_bat(path,server_name))

        
        chatbot_deactive_btn = QPushButton(f'挂起', self)
        chatbot_deactive_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        chatbot_deactive_btn.clicked.connect(lambda checked, path=os.path.join(CHATBOT_PATH,'chatbot_deactivate.bat') , server_name='chatbot' : self.execute_bat(path,server_name))

        
        chatbot_offline_btn = QPushButton(f'下线', self)
        chatbot_offline_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        chatbot_offline_btn.clicked.connect(lambda checked, path=os.path.join(CHATBOT_PATH,'chatbot_down.bat') , server_name='chatbot' : self.execute_bat(path,server_name))

        
        chatbot_redis_show_btn = QPushButton(f'显示对话请求', self)
        chatbot_redis_show_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        chatbot_redis_show_btn.clicked.connect(lambda checked, path='chatbot_ask' , server_name='chatbot_show' : self.execute_bat(path,server_name))

        
        chatbot_redis_show_down_btn = QPushButton(f'显示对话回答', self)
        chatbot_redis_show_down_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        chatbot_redis_show_down_btn.clicked.connect(lambda checked, path='chatbot_answer' , server_name='chatbot_show' : self.execute_bat(path,server_name))


        chatbot_text_send_btn = QPushButton(f'发送对话', self)
        chatbot_text_send_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        chatbot_text_send_btn.clicked.connect(lambda checked, path='chatbot_ask' , server_name='chatbot_send' : self.execute_bat(path,server_name))

        
        # 将按钮加入列表  
        self.chatbot_buttons.append(chatbot_start_btn) 
        self.chatbot_buttons.append(chatbot_activate_btn)  
        self.chatbot_buttons.append(chatbot_deactive_btn)  
        self.chatbot_buttons.append(chatbot_offline_btn)  
        
        self.chatbot_show_buttons.append(chatbot_redis_show_btn)
        self.chatbot_show_buttons.append(chatbot_redis_show_down_btn)
        
        # 添加到布局
        chatbot_layout.addWidget(chatbot_start_btn)
        chatbot_layout.addWidget(chatbot_activate_btn)
        chatbot_layout.addWidget(chatbot_deactive_btn)
        chatbot_layout.addWidget(chatbot_offline_btn)
        chatbot_layout.addWidget(chatbot_redis_show_btn)
        chatbot_layout.addWidget(chatbot_redis_show_down_btn)
        
        
        chatbot_label = QLabel('大语言模型对话服务', self)        
        # 或者创建一个可以多行显示的 QTextEdit
        self.chatbot_text_edit = QTextEdit(self)

        self.chatbot_text_send_edit = QTextEdit(self)

        chatbot_container = QWidget(self)  
        chatbot_container.setLayout(chatbot_layout)
        
        
        
        
        
        
        
        
        
        
        #------------------------------------------------------------------------- ai deamon  ----------------------------------------------------
        
        
        daemon_layout = QHBoxLayout()
        
        # 按钮和状态灯  
        self.daemon_buttons = []
        #self.reid_show_buttons = []
        
        # 创建按钮  
        daemon_start_btn = QPushButton(f'启动守护进程', self)
        daemon_start_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        daemon_start_btn.clicked.connect(lambda checked, path=os.path.join(DAEMON_PATH,'ai_start.bat') , server_name='daemon' : self.execute_bat(path,server_name))
        
        
        '''
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

        '''
        daemon_offline_btn = QPushButton(f'AI系统下线', self)
        daemon_offline_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        daemon_offline_btn.clicked.connect(lambda checked, path=os.path.join(DAEMON_PATH,'ai_down.bat') , server_name='daemon' : self.execute_bat(path,server_name))

        
        daemon_refresh_btn = QPushButton(f'清理守护残余', self)
        daemon_refresh_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        daemon_refresh_btn.clicked.connect(lambda checked, path=os.path.join(DAEMON_PATH,'ai_refresh.bat') , server_name='daemon' : self.execute_bat(path,server_name))

        
        daemon_set_online_btn = QPushButton(f'设置上线', self)
        daemon_set_online_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        daemon_set_online_btn.clicked.connect(lambda checked, path=os.path.join(DAEMON_PATH,'ai_online.bat') , server_name='daemon' : self.execute_bat(path,server_name))

        

        
        # 将按钮加入列表  
        self.daemon_buttons.append(daemon_start_btn) 
        self.daemon_buttons.append(daemon_offline_btn)  
        self.daemon_buttons.append(daemon_refresh_btn) 
        self.daemon_buttons.append(daemon_set_online_btn)  
        
        
        # 添加到布局
        daemon_layout.addWidget(daemon_start_btn)
        daemon_layout.addWidget(daemon_offline_btn)
        daemon_layout.addWidget(daemon_refresh_btn)
        daemon_layout.addWidget(daemon_set_online_btn)
        
        
        daemon_label = QLabel('AI守护系统控制', self)
        
        daemon_container = QWidget(self)  
        daemon_container.setLayout(daemon_layout)
        
        
        
        
        
        
        #------------------------------------------------------------------------- score -------------------------------------------
        
        
        score_layout = QHBoxLayout()
        
        # 按钮和状态灯  
        self.score_buttons = []
        self.score_show_buttons = []
        
        # 创建按钮  
        score_start_btn = QPushButton(f'启动AI评分', self)
        score_start_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        score_start_btn.clicked.connect(lambda checked, path=os.path.join(SCORE_PATH,'score_start.bat') , server_name='score' : self.execute_bat(path,server_name))
        
        score_activate_btn = QPushButton(f'激活', self)
        score_activate_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        score_activate_btn.clicked.connect(lambda checked, path=os.path.join(SCORE_PATH,'score_activate.bat') , server_name='score' : self.execute_bat(path,server_name))

        
        score_deactive_btn = QPushButton(f'挂起', self)
        score_deactive_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        score_deactive_btn.clicked.connect(lambda checked, path=os.path.join(SCORE_PATH,'score_deactivate.bat') , server_name='score' : self.execute_bat(path,server_name))

        
        score_offline_btn = QPushButton(f'下线', self)
        score_offline_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        score_offline_btn.clicked.connect(lambda checked, path=os.path.join(SCORE_PATH,'score_down.bat') , server_name='score' : self.execute_bat(path,server_name))

        
        score_cfg_redis_show_btn = QPushButton(f'显示课程设置', self)
        score_cfg_redis_show_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        score_cfg_redis_show_btn.clicked.connect(lambda checked, path='score_cfg' , server_name='score_show' : self.execute_bat(path,server_name))

        
        score_redis_show_btn = QPushButton(f'显示课程分数', self)
        score_redis_show_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        score_redis_show_btn.clicked.connect(lambda checked, path='score_result' , server_name='score_show' : self.execute_bat(path,server_name))


        score_cfg_send_btn = QPushButton(f'发送课程设置', self)
        score_cfg_send_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        score_cfg_send_btn.clicked.connect(lambda checked, path='score_cfg' , server_name='score_send' : self.execute_bat(path,server_name))

        
        # 将按钮加入列表  
        self.score_buttons.append(score_start_btn) 
        self.score_buttons.append(score_activate_btn)  
        self.score_buttons.append(score_deactive_btn)  
        self.score_buttons.append(score_offline_btn)  
        
        self.score_show_buttons.append(score_cfg_redis_show_btn)
        self.score_show_buttons.append(score_redis_show_btn)
        
        # 添加到布局
        score_layout.addWidget(score_start_btn)
        score_layout.addWidget(score_activate_btn)
        score_layout.addWidget(score_deactive_btn)
        score_layout.addWidget(score_offline_btn)
        score_layout.addWidget(score_cfg_redis_show_btn)
        score_layout.addWidget(score_redis_show_btn)
        
        
        score_label = QLabel('AI评分服务', self)        
        # 或者创建一个可以多行显示的 QTextEdit
        self.score_text_edit = QTextEdit(self)

        self.score_text_send_edit = QTextEdit(self)

        score_container = QWidget(self)  
        score_container.setLayout(score_layout)
        
        
        
        
        
        
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
        
        
        
        
        
        
        #-------------------------------------------------------------------------servo_motor_drive_platform_recognition -------------------------------------------
        
        
        smdpr_layout = QHBoxLayout()
        
        # 按钮和状态灯  
        self.smdpr_buttons = []
        self.smdpr_show_buttons = []
        
        # 创建按钮  
        smdpr_start_btn = QPushButton(f'启动伺服电机平台识别', self)
        smdpr_start_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        smdpr_start_btn.clicked.connect(lambda checked, path=os.path.join(SMDPR_PATH,'smdpr_start.bat') , server_name='smdpr' : self.execute_bat(path,server_name))
        
        smdpr_activate_btn = QPushButton(f'激活', self)
        smdpr_activate_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        smdpr_activate_btn.clicked.connect(lambda checked, path=os.path.join(SMDPR_PATH,'smdpr_activate.bat') , server_name='smdpr' : self.execute_bat(path,server_name))

        
        smdpr_deactive_btn = QPushButton(f'挂起', self)
        smdpr_deactive_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        smdpr_deactive_btn.clicked.connect(lambda checked, path=os.path.join(SMDPR_PATH,'smdpr_deactivate.bat') , server_name='smdpr' : self.execute_bat(path,server_name))

        
        smdpr_offline_btn = QPushButton(f'下线', self)
        smdpr_offline_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        smdpr_offline_btn.clicked.connect(lambda checked, path=os.path.join(SMDPR_PATH,'smdpr_down.bat') , server_name='smdpr' : self.execute_bat(path,server_name))

        
        smdpr_redis_show_btn = QPushButton(f'显示', self)
        smdpr_redis_show_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        smdpr_redis_show_btn.clicked.connect(lambda checked, path=os.path.join(SMDPR_PATH,'smdpr_redis_show.bat') , server_name='smdpr_show' : self.execute_bat(path,server_name))

        
        smdpr_redis_show_down_btn = QPushButton(f'关闭显示', self)
        smdpr_redis_show_down_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        smdpr_redis_show_down_btn.clicked.connect(lambda checked, path=os.path.join(SMDPR_PATH,'smdpr_show_down.bat') , server_name='smdpr_show' : self.execute_bat(path,server_name))

        

        
        
        # 将按钮加入列表  
        self.smdpr_buttons.append(smdpr_start_btn) 
        self.smdpr_buttons.append(smdpr_activate_btn)  
        self.smdpr_buttons.append(smdpr_deactive_btn)  
        self.smdpr_buttons.append(smdpr_offline_btn)  
        
        self.smdpr_show_buttons.append(smdpr_redis_show_btn)
        self.smdpr_show_buttons.append(smdpr_redis_show_down_btn)
        
        # 添加到布局
        smdpr_layout.addWidget(smdpr_start_btn)
        smdpr_layout.addWidget(smdpr_activate_btn)
        smdpr_layout.addWidget(smdpr_deactive_btn)
        smdpr_layout.addWidget(smdpr_offline_btn)
        smdpr_layout.addWidget(smdpr_redis_show_btn)
        smdpr_layout.addWidget(smdpr_redis_show_down_btn)
        
        
        smdpr_label = QLabel('伺服电机平台识别服务', self)
        
        smdpr_container = QWidget(self)  
        smdpr_container.setLayout(smdpr_layout)
        
        
        #-------------------------------------------------------------------------servo_motor_drive_platform_trajectory -------------------------------------------
        
        
        smdpj_layout = QHBoxLayout()
        
        # 按钮和状态灯  
        self.smdpj_buttons = []
        self.smdpj_show_buttons = []
        
        # 创建按钮  
        smdpj_start_btn = QPushButton(f'伺服电机轨迹生成', self)
        smdpj_start_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        smdpj_start_btn.clicked.connect(lambda checked, path=os.path.join(SMDPJ_PATH,'smdpj_start.bat') , server_name='smdpj' : self.execute_bat(path,server_name))
        
        smdpj_activate_btn = QPushButton(f'激活', self)
        smdpj_activate_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        smdpj_activate_btn.clicked.connect(lambda checked, path=os.path.join(SMDPJ_PATH,'smdpj_activate.bat') , server_name='smdpj' : self.execute_bat(path,server_name))

        
        smdpj_deactive_btn = QPushButton(f'挂起', self)
        smdpj_deactive_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        smdpj_deactive_btn.clicked.connect(lambda checked, path=os.path.join(SMDPJ_PATH,'smdpj_deactivate.bat') , server_name='smdpj' : self.execute_bat(path,server_name))

        
        smdpj_offline_btn = QPushButton(f'下线', self)
        smdpj_offline_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        smdpj_offline_btn.clicked.connect(lambda checked, path=os.path.join(SMDPJ_PATH,'smdpj_down.bat') , server_name='smdpj' : self.execute_bat(path,server_name))

        
        smdpj_redis_show_btn = QPushButton(f'显示', self)
        smdpj_redis_show_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        smdpj_redis_show_btn.clicked.connect(lambda checked, path=os.path.join(SMDPJ_PATH,'smdpj_redis_show.bat') , server_name='smdpj_show' : self.execute_bat(path,server_name))

        
        smdpj_redis_show_down_btn = QPushButton(f'关闭显示', self)
        smdpj_redis_show_down_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        smdpj_redis_show_down_btn.clicked.connect(lambda checked, path=os.path.join(SMDPJ_PATH,'smdpj_show_down.bat') , server_name='smdpj_show' : self.execute_bat(path,server_name))

        
        smpdj_id_send_btn = QPushButton(f'发送轨迹ID设置', self)
        smpdj_id_send_btn.setStyleSheet("QPushButton {"
                                  "  background-color: rgb(255, 255, 255);"
                                  "}"
                                  "QPushButton:hover {"
                                  "  background-color: rgb(0, 255, 0);"
                                  "}")
        smpdj_id_send_btn.clicked.connect(lambda checked, path='smpdj_id' , server_name='smpdj_id_send' : self.execute_bat(path,server_name))
        
        
        # 将按钮加入列表  
        self.smdpj_buttons.append(smdpj_start_btn) 
        self.smdpj_buttons.append(smdpj_activate_btn)  
        self.smdpj_buttons.append(smdpj_deactive_btn)  
        self.smdpj_buttons.append(smdpj_offline_btn)  
        
        self.smdpj_show_buttons.append(smdpj_redis_show_btn)
        self.smdpj_show_buttons.append(smdpj_redis_show_down_btn)
        
        # 添加到布局
        smdpj_layout.addWidget(smdpj_start_btn)
        smdpj_layout.addWidget(smdpj_activate_btn)
        smdpj_layout.addWidget(smdpj_deactive_btn)
        smdpj_layout.addWidget(smdpj_offline_btn)
        smdpj_layout.addWidget(smdpj_redis_show_btn)
        smdpj_layout.addWidget(smdpj_redis_show_down_btn)
        
        
        smdpj_label = QLabel('伺服电机平台轨迹生成服务', self)
        self.smpdj_text_edit = QTextEdit(self)
        smdpj_container = QWidget(self)  
        smdpj_container.setLayout(smdpj_layout)
        
        
        
        
        
        ################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
        
        
        
        
        split_label0 = QLabel('----------------------------------------------------', self)
        split_label1 = QLabel('----------------------------------------------------', self)
        split_label1a = QLabel('----------------------------------------------------', self)
        split_label2 = QLabel('----------------------------------------------------', self)
        split_label3 = QLabel('----------------------------------------------------', self)
        split_label4 = QLabel('----------------------------------------------------', self)
        split_label5 = QLabel('----------------------------------------------------', self)
        split_label6 = QLabel('----------------------------------------------------', self)
        split_label7 = QLabel('----------------------------------------------------', self)
        split_label8 = QLabel('----------------------------------------------------', self)
        split_label9 = QLabel('----------------------------------------------------', self)
        # 将包含子布局的QWidget添加到主布局中  
        
        mainLayout.addWidget(daemon_label)
        mainLayout.addWidget(daemon_container)
        mainLayout.addWidget(split_label0)
        
        
        mainLayout.addWidget(camera_label)
        mainLayout.addWidget(camera_container)
        mainLayout.addWidget(split_label1)
        
        mainLayout.addWidget(camera_top_label)
        mainLayout.addWidget(camera_top_container)
        mainLayout.addWidget(split_label1a)
        
        mainLayout.addWidget(face_label)
        mainLayout.addWidget(face_container)
        mainLayout.addWidget(split_label2)
        
        mainLayout.addWidget(feature_collect_label)
        mainLayout.addWidget(feature_collect_container)
        mainLayout.addWidget(split_label3)
        
        mainLayout.addWidget(reid_label)
        mainLayout.addWidget(reid_container)
        mainLayout.addWidget(split_label4)
        
        mainLayout.addWidget(tts_label)
        mainLayout.addWidget(tts_container)
        mainLayout.addWidget(self.tts_text_edit)
        mainLayout.addWidget(self.tts_text_send_edit)
        mainLayout.addWidget(tts_text_send_btn)
        mainLayout.addWidget(split_label5)
        
        mainLayout.addWidget(asr_label)
        mainLayout.addWidget(asr_container)
        mainLayout.addWidget(self.asr_text_edit)
        mainLayout.addWidget(self.asr_text_send_edit)
        mainLayout.addWidget(asr_text_send_btn)
        mainLayout.addWidget(split_label6)
        
        mainLayout.addWidget(chatbot_label)
        mainLayout.addWidget(chatbot_container)
        mainLayout.addWidget(self.chatbot_text_edit)
        mainLayout.addWidget(self.chatbot_text_send_edit)
        mainLayout.addWidget(chatbot_text_send_btn)
        mainLayout.addWidget(split_label7)
        
        
        mainLayout.addWidget(score_label)
        mainLayout.addWidget(score_container)
        mainLayout.addWidget(self.score_text_edit)
        mainLayout.addWidget(self.score_text_send_edit)
        mainLayout.addWidget(score_cfg_send_btn)
        mainLayout.addWidget(split_label8)
        
        mainLayout.addWidget(smdpr_label)
        mainLayout.addWidget(smdpr_container)
        mainLayout.addWidget(split_label9)
        
        
        mainLayout.addWidget(smdpj_label)
        mainLayout.addWidget(smdpj_container)
        mainLayout.addWidget(self.smpdj_text_edit)
        mainLayout.addWidget(smpdj_id_send_btn)
        
        
        # 创建一个QLabel并添加到主布局中  
        #label = QLabel('这是一个标签', self)  
        #mainLayout.addWidget(label)  
  
        # 创建一个QWidget作为滚动区域的内容  
        content_widget = QWidget()  
        content_widget.setLayout(mainLayout)  
        
        # 创建一个QScrollArea  
        scroll_area = QScrollArea()  
        scroll_area.setWidgetResizable(True)  # 允许滚动区域的内容大小变化  
        scroll_area.setWidget(content_widget)  # 设置滚动区域的内容
         
        # 设置窗口的主布局  
        #self.setLayout(mainLayout) 
        
        # 设置窗口的布局，并将滚动区域添加到窗口中  
        self.setLayout(QVBoxLayout())  
        self.layout().addWidget(scroll_area)  
  
    def execute_bat(self, path , server_name):
        if server_name == 'camera':
            buttons = self.camera_buttons
        if server_name == 'camera_show':
            buttons = self.camera_show_buttons   
        if server_name == 'camera_top':
            buttons = self.camera_top_buttons
        if server_name == 'camera_top_show':
            buttons = self.camera_top_show_buttons   
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
        if server_name == 'tts':
            buttons = self.tts_buttons
        if server_name == 'tts_show':
            buttons = self.tts_show_buttons
            from code.ai_server.text_to_speech.config import EnvConfig
            env = EnvConfig()
            #result = redis_show(path)
            r = redis.Redis(host='localhost', port=6379, db=0)  
            if path == 'tts_text':
                key = env.redis_text_flag  
            else:
                key = env.redis_sound_flag
            result_text = ""
            list_values = r.lrange(key, 0, -1)
            for value in list_values:
                dict_value = json.loads(value)  
                result_text += dict_value['seq']
                result_text += ' '
                result_text += dict_value['text']    
                if 'path' in dict_value.keys():
                    result_text += ' '
                    result_text += dict_value['path']
                result_text += '\r\n'
            self.tts_text_edit.setText(result_text)
                
        if server_name == 'tts_send':
            text = self.tts_text_send_edit.toPlainText()
            if text!="":
                from code.ai_server.text_to_speech.config import EnvConfig
                env = EnvConfig()
                r = redis.Redis(host='localhost', port=6379, db=0)  
                def get_now_YMDhmsms():
                    timestamp = time.time()
                    dt_object = datetime.datetime.fromtimestamp(timestamp)  
                    # 获取毫秒部分  
                    milliseconds = int((timestamp - int(timestamp)) * 1000)  
                    # 格式化日期和时间字符串，并手动添加毫秒  
                    formatted_time = dt_object.strftime("%Y%m%d%H%M%S") + str(milliseconds).zfill(3)  
                    #print(formatted_time)  # 输出形如：2023-07-19 15:30:45.123
                    return formatted_time
                def set_tts_text(redis_object,redis_key,text):
                    time_str = get_now_YMDhmsms()
                    push_dict = {
                        'seq':time_str,
                        'text':text,
                        'time':time_str
                    }
                    #推送到Redis  
                    try:
                        redis_object.rpush(redis_key, json.dumps(push_dict))
                    except Exception as e:
                        print (e)
                set_tts_text(r,env.redis_text_flag,text)
            return
        
        
        if server_name == 'asr':
            buttons = self.asr_buttons
                      
        
        if server_name == 'asr_show':
            buttons = self.asr_show_buttons
            from code.ai_server.voice_to_word.config import EnvConfig
            env = EnvConfig()
            r = redis.Redis(host='localhost', port=6379, db=0)  
            if path == 'asr_text':
                key = env.redis_text_flag  
            else:
                key = env.redis_sound_flag
            result_text = ""
            list_values = r.lrange(key, 0, -1)
            for value in list_values:
                dict_value = json.loads(value)  
                result_text += dict_value['seq']
                result_text += ' '
                result_text += dict_value['path']    
                if 'text' in dict_value.keys():
                    result_text += ' '
                    result_text += dict_value['text']
                result_text += '\r\n'
            self.asr_text_edit.setText(result_text)
        
        if server_name == 'asr_send':
            text = self.asr_text_send_edit.toPlainText()
            if not os.path.exists(text):
                self.asr_text_send_edit.setText('No file exist!')
                return
            if text!="":
                from code.ai_server.voice_to_word.config import EnvConfig
                env = EnvConfig()
                r = redis.Redis(host='localhost', port=6379, db=0)  
                def get_now_YMDhmsms():
                    timestamp = time.time()
                    dt_object = datetime.datetime.fromtimestamp(timestamp)  
                    # 获取毫秒部分  
                    milliseconds = int((timestamp - int(timestamp)) * 1000)  
                    # 格式化日期和时间字符串，并手动添加毫秒  
                    formatted_time = dt_object.strftime("%Y%m%d%H%M%S") + str(milliseconds).zfill(3)  
                    #print(formatted_time)  # 输出形如：2023-07-19 15:30:45.123
                    return formatted_time
                        
                def set_asr_voice(redis_object,redis_key,path):
                    time_str = get_now_YMDhmsms()
                    push_dict = {
                        'seq':time_str,
                        'path':path,
                        'time':time_str
                    }
                    #推送到Redis  
                    try:
                        redis_object.rpush(redis_key, json.dumps(push_dict))
                    except Exception as e:
                        print (e)
                set_asr_voice(r,env.redis_sound_flag,text)
            return

        
        
        if server_name == 'chatbot':
            buttons = self.chatbot_buttons
            
        if server_name == 'chatbot_show':
            buttons = self.chatbot_show_buttons
            from code.ai_server.chatbot.config import EnvConfig
            env = EnvConfig()
            r = redis.Redis(host='localhost', port=6379, db=0)  
            if path == 'chatbot_ask':
                key = env.redis_ask_flag 
            else:
                key = env.redis_answer_flag
            result_text = ""
            list_values = r.lrange(key, 0, -1)
            for value in list_values:
                dict_value = json.loads(value)  
                result_text += dict_value['seq']
                result_text += ' '
                result_text += dict_value['ask']    
                if 'answer' in dict_value.keys():
                    result_text += ' '
                    result_text += dict_value['answer']
                result_text += '\r\n'
            self.chatbot_text_edit.setText(result_text)
        
        if server_name == 'chatbot_send':
            text = self.chatbot_text_send_edit.toPlainText()
            if text == '':
                self.chatbot_text_send_edit.setText('words are empty!')
                return
            else:
                from code.ai_server.chatbot.config import EnvConfig
                env = EnvConfig()
                r = redis.Redis(host='localhost', port=6379, db=0)  
                def get_now_YMDhmsms():
                    timestamp = time.time()
                    dt_object = datetime.datetime.fromtimestamp(timestamp)  
                    # 获取毫秒部分  
                    milliseconds = int((timestamp - int(timestamp)) * 1000)  
                    # 格式化日期和时间字符串，并手动添加毫秒  
                    formatted_time = dt_object.strftime("%Y%m%d%H%M%S") + str(milliseconds).zfill(3)  
                    #print(formatted_time)  # 输出形如：2023-07-19 15:30:45.123
                    return formatted_time
                        
                def set_chatbot_ask(redis_object,redis_key,ask_str):
                    time_str = get_now_YMDhmsms()
                    push_dict = {
                        'seq':time_str,
                        'ask':ask_str,
                        'time':time_str
                    }
                    #推送到Redis  
                    try:
                        redis_object.rpush(redis_key, json.dumps(push_dict))
                    except Exception as e:
                        print (e)
                set_chatbot_ask(r,env.redis_ask_flag,text)
            return
        
        if server_name == 'daemon':
            buttons = self.daemon_buttons
        
        if server_name == 'score':
            buttons = self.score_buttons
        
        if server_name == 'score_show':
            buttons = self.score_show_buttons
            from code.ai_server.score.config import EnvConfig
            env = EnvConfig()
            r = redis.Redis(host='localhost', port=6379, db=0)  
            
            redis_text = ""
            if path == 'score_cfg':
                key = env.project_cfg_key 
                #redis_text = r.get(key).decode('utf-8')
            else:
                key = env.project_scores_key
            redis_text = r.get(key).decode('utf-8')
                #redis_text = r.lindex(key, -1)
            if redis_text=="":
                self.score_text_edit.setText("redis empty!")
            else:
                try:
                    result_text = ""
                    print (redis_text)
                    result_dict = json.loads(redis_text)  
                    print (result_dict)
                    for r_key in result_dict.keys():
                        result_text+= str(r_key)
                        result_text+= "   "
                        result_text+= str(result_dict[r_key])
                        result_text += '\r\n'
                    self.score_text_edit.setText(result_text) 
                except Exception as e:
                    print (e)
                    self.score_text_edit.setText(str(e))
            
        if server_name == 'score_send':
            text = self.score_text_send_edit.toPlainText()
            if text == '':
                self.score_text_send_edit.setText('words are empty!')
                return
            else:
                from code.ai_server.score.config import EnvConfig
                env = EnvConfig()
                r = redis.Redis(host='localhost', port=6379, db=0)  
                #推送到Redis  
                try:
                    r.set(env.project_cfg_key, text)
                except Exception as e:
                    print (e)
                    self.score_text_send_edit.setText(str(e))
            return
        
        if server_name == 'smdpr':
            buttons = self.smdpr_buttons
        if server_name == 'smdpr_show':
            buttons = self.smdpr_show_buttons 
            
        if server_name == 'smdpj':
            buttons = self.smdpj_buttons
        if server_name == 'smdpj_show':
            buttons = self.smdpj_show_buttons 
            
        if server_name == 'smpdj_id_send':
            text = self.smpdj_text_edit.toPlainText()
            if text!="":
                from code.ai_server.platform_trajectory.config import EnvConfig
                env = EnvConfig()
                r = redis.Redis(host='localhost', port=6379, db=0)  
                #推送到Redis  
                try:
                    r.set(env.trajectory_id_key, text)
                except Exception as e:
                    print (e)
                    self.smpdj_text_edit.setText(str(e))
            return 
                    
            
        ################################################################################################################################################################    
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