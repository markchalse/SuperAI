Hello I am Super AI.

quick clone

git clone https://mirror.ghproxy.com/https://github.com/markchalse/SuperAI.git


# 脚本路径说明
`/script`

一些涉及整个系统的，QT需要启动的脚本

## 启动脚本
`/script/start.bat`

QT启动时执行的脚本，这个文件中，会拉起全部的AI进程

# 代码路径说明

## 数据感知共享代码
`/code/data_sensor`

每个类型传感器在此路径下创建文件夹项目，上传数据至redis数据库

## AI服务类代码
`/code/ai_server`

每个类型的AI服务在此路径下创建文件夹项目，从redis获取数据，并上传处理后的信息