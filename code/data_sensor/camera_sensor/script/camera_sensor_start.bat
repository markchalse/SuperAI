@echo off
set MODE=debug
if "%MODE%"=="debug" (
    CALL E:\anaconda\Scripts\activate.bat E:\anaconda
    CALL conda activate scene_learning_1
    python F:\workspace\majun\zhiyuanchuang_space\ai_code\superai\SuperAI\code\data_sensor\camera_sensor\main.py
) else (
    CALL D:\software\computer\Anaconda\Scripts\activate.bat D:\software\computer\Anaconda
    CALL conda activate scene_learning_1
    python G:\workspace\majun\code\SuperAI\code\data_sensor\camera_sensor\main.py
)
conda deactivate
pause