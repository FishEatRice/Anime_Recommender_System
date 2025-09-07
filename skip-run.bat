@echo off
:START
cls
streamlit run main.py

:: If the script ends, ask if you want to restart
echo.
set /p restart="Server stopped. Do you want to stop the server? (y/n): "

if /i "%restart%"=="n" (
    goto START
) else (
    exit
)
