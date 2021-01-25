@echo off

if "X%COG_INSTALL_PATH%" == "X" goto nocogpath
goto cogpath

:nocogpath
    set UNSET_COG_INSTALL_PATH=1
    set COG_INSTALL_PATH=..
    if NOT EXIST "%COG_INSTALL_PATH%\lib\cog-karajan-0.36-dev.jar" goto nocogpath15
    goto cogpath
	
:nocogpath15
	if NOT EXIST "%COG_INSTALL_PATH%\lib\cog.jar" goto nocogpath2
	goto cogpath
    
:nocogpath2
    rem test for expansion extensions first, so that we don't enter an infinite loop
    set PARTIAL_PATH=test
    set PARTIAL_PATH=%PARTIAL_PATH:~-2%
    if NOT "%PARTIAL_PATH%" == "st" goto nocogpath3
    set PARTIAL_PATH=%~f0
    set FIRST_BACKSLASH=1
    
:loop
    set LAST_CHAR=%PARTIAL_PATH:~-1%
    set PARTIAL_PATH=%PARTIAL_PATH:~0,-1%
    if "%LAST_CHAR%" == "\" goto found
    if "X%PARTIAL_PATH%" == "X" goto nocogpath3
    goto loop

    
:found
    if "%FIRST_BACKSLASH%" == "0" goto found2
    set FIRST_BACKSLASH=0
    goto loop
     
:found2
    set COG_INSTALL_PATH=%PARTIAL_PATH%
    if NOT EXIST "%COG_INSTALL_PATH%\lib\cog-karajan-0.36-dev.jar" goto nocogpath25
    goto cogpath
	
:nocogpath25
	if NOT EXIST "%COG_INSTALL_PATH%\lib\cog.jar" goto nocogpath3
	goto cogpath
    
:nocogpath3
    echo Error: COG_INSTALL_PATH not set and all attempts at guessing it failed
    goto end

:cogpath

	set OPTS=%COG_OPTS% -Djava.endorsed.dirs="%COG_INSTALL_PATH%\lib\endorsed"

	set LOCALCLASSPATH=%CLASSPATH%;%COG_INSTALL_PATH%\etc
	
	for %%J in ("%COG_INSTALL_PATH%\lib\*.jar") DO call :setpath %%J
    
    set SAVECLASSPATH=%CLASSPATH%
    set CLASSPATH=%LOCALCLASSPATH%
    java %OPTS% org.globus.cog.karajan.workflow.service.Service %*
    set CLASSPATH=%SAVECLASSPATH%

:end
    if "%UNSET_COG_INSTALL_PATH%"=="1" goto restore
    goto done
    
:setpath
    set LOCALCLASSPATH=%LOCALCLASSPATH%;%*
    goto done

:restore
    set COG_INSTALL_PATH=
    set PARTIAL_PATH=
    set LAST_CHAR=
    set UNSET_COG_INSTALL_PATH=
    set FIRST_BAKSLASH=

:done
