@echo off

REM path to pyton executable
set PYTHON_PATH=C:\Users\Administrator\Documents\python_env\email_env\Scripts\python.exe

REM path to python script
set PYTHON_SCRIPT=C:\Users\Administrator\Documents\python_env\email_env\main.py

REM path to log file
set LOG_FILE=C:\Users\Administrator\Documents\python_env\email_env\log_file.log

echo Starting email script... >> %LOG_FILE%
echo Starting email script...

%PYTHON_PATH% %PYTHON_SCRIPT%

IF %ERRORLEVEL% EQU 0(
    echo Email script completed successfully. Stopping script. >> %LOG_FILE%
    echo Email script completed successfully. Stopping script.
) ELSE (
    echo Email script encountered an error. >> %LOG_FILE%
    echo Email script encountered an error. 
)

