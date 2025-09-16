@echo off
setlocal enabledelayedexpansion
if "%~4"=="" (
    echo Usage: upload.bat [file] [name] [arch] [version]
    exit /b 1
)
set "HOME=%~dp0"
set "name=%2"
set "arch=%3"
set "version=%4"
mkdir "%HOME%%name%"
move /y "%HOME%%name%\%name%_%arch%_latest.zip" "%HOME%%name%\%name%_%arch%_%version%.zip"
copy /y %1 "%HOME%%name%\%name%_%arch%_latest.zip"
endlocal