@echo off
echo -------------load env------------->> load-env.log
:: 获取批处理文件所在的目录  
set "batDir=%~dp0"  
:: 构造env.txt文件的完整路径  
set "envFilePath=%batDir%env.txt" 

:: 检查env.txt文件是否存在  
if not exist "%envFilePath%" (  
    echo env.txt not found at %envFilePath%  
    pause  
    exit /b 1  
)  

for /f "delims== tokens=1* eol=#" %%i in (%envFilePath%) do (
	set %%i=%%j
	echo %%i=%%j>> load-env.log
)
echo -------------load env------------->> load-env.log
set activate_path=%anaconda_path%\Scripts\activate.bat
CALL %activate_path% %anaconda_path%
CALL conda activate %conda_env_name%
python %code_base_path%\code\ai_server\servo_motor_drive_platform_recognition\thread_controller.py --func activate
conda deactivate