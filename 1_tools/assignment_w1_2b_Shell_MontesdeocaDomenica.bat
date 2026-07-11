:: *****************************************************************
:: author: Domenica Montesdeoca
:: date: 08/07/2026
:: *****************************************************************

:: ADDS custom script paths
set "SCRIPT_PATH=F:\TDA_Python_Adv\Scripts"
set "PYTHONPATH=%SCRIPT_PATH%"%PYTHONPATH%;

:: ADDITIONAL overwrites (paths, menus, ...)
set "MAYA_PLUGINS_PATH=%SCRIPT_PATH%\Plugins\;%MAYA_PLUGINS_PATH%"

:: STARTS a DCC of your choice (Maya, 3ds Max, Nuke, Houdini, ...)
start "" "C:\Program Files\Autodesk\Maya2023\bin\maya.exe"