@echo off
REM �÷���ctcmd_trim_space.bat �ļ���
setlocal enabledelayedexpansion

if "%~1"=="" (
    echo ���ṩҪ������ļ���
    exit /b 1
)

set "infile=%~1"
set "outfile=%infile%.trimmed"

(for /f "usebackq delims=" %%a in ("%infile%") do (
    set "line=%%a"
    set "line=!line: =!"
    for /f "tokens=* delims= " %%b in ("!line!") do (
        set "line=%%a"
        REM �Ƴ���β�ո�
        for /f "tokens=* delims=" %%c in ("!line!") do (
            set "line=%%c"
            setlocal enabledelayedexpansion
            set "line=!line!"
            for /f "tokens=* delims=" %%d in ("!line!") do (
                set "line=%%d"
                REM ���������Ƴ���β�ո�
                set "line=!line!"
                set "line=!line: =!"
                echo !line!
            )
            endlocal
        )
    )
)) > "%outfile%"

echo �Ѵ�����ϣ�����ļ���%outfile%