@echo off
CALL E:\anaconda\Scripts\activate.bat E:\anaconda
::CALL D:\software\computer\Anaconda\Scripts\activate.bat D:\software\computer\Anaconda
CALL conda activate scene_learning_1
python F:\workspace\majun\zhiyuanchuang_space\ai_code\superai\SuperAI\code\data_sensor\camera_sensor\redis_show.py
::python G:\workspace\majun\code\zhiyuanchuang_scene_learning\zhiyuanchuang_scene_learning\code\project\student_persona\project\dynamic_task.py
conda deactivate
pause