@echo off
setlocal enabledelayedexpansion
if "%~4"=="" (
    echo Usage: upload.bat [file] [name] [arch] [last_will_change_version]
    exit /b 1
)
set "HOME=%~dp0"
set "name=%2"
set "arch=%3"
set "version=%4"
for /f "tokens=* delims=" %%a in ('type "%HOME%\all.ctcmd"') do (
    set "line=%%a"
    if not "!line!"=="" if not "!line:~0,2!"=="//" (
        for /f "tokens=1,2 delims=@" %%b in ("!line!") do (
            @REM echo 处理行: !line!
            @REM echo @前部分: %%b
            @REM echo @后部分: %%c
            @REM echo.
            if "%name%"=="%%b" (
                echo Found matching name: %%b
                goto skip
            ) else (
                echo %name%@https://raw.githubusercontent.com/xingguangcuican6666/ctcmd_repo/refs/heads/main/%name% >> "%HOME%\all.ctcmd"
                goto skip
            )
        )
    )
)
:skip
mkdir "%HOME%%name%"
move /y "%HOME%%name%\%name%_%arch%_latest.zip" "%HOME%%name%\%name%_%arch%_%version%.zip"
copy /y %1 "%HOME%%name%\%name%_%arch%_latest.zip"
endlocal