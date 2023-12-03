@echo off
setlocal enabledelayedexpansion

set "sourcePath=F:\job\hoaphatzRender\feed1\shot31\env\0033.png"
set "targetPath=F:\job\hoaphatzRender\feed1\shot31\env\"

for /L %%i in (33, 1, 120) do (
    set "sourceFile=0033.png"
    set "targetFile=00%%i.png"
    set "targetFile=!targetFile:~-8,8!"

    copy "!sourcePath!" "!targetPath!!targetFile!" > nul
    echo Copied !targetFile!
)

endlocal
