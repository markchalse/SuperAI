@echo off
echo -------------load env------------->> load-env.log
for /f "delims== tokens=1* eol=#" %%i in (env.txt) do (
	set %%i=%%j
	echo %%i=%%j>> load-env.log
)
echo -------------load env------------->> load-env.log
set activate_path=%anaconda_path%\Scripts\activate.bat
CALL %activate_path% %anaconda_path%
CALL conda activate %conda_env_name%
python %code_base_path%\ai_demo.py
conda deactivate
pause