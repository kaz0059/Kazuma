REM start_console.bat - Launch console version
@echo off
cd /d %~dp0
call renenv\Scripts\activate
python assistant.py
pause

REM start_gui.bat - Launch GUI version  
@echo off
cd /d %~dp0
call renenv\Scripts\activate
python gui_assistant.py
pause

REM start_env.bat - Open environment for development
@echo off  
cd /d %~dp0
call renenv\Scripts\activate
echo AI Assistant Development Environment
echo ===================================
echo Console: python assistant.py
echo GUI:     python gui_assistant.py
echo ===================================
cmd