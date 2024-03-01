@echo off
setlocal enabledelayedexpansion

set "videoPath=\\192.168.0.7\senshu\Hoc hanh\acacdemy\Coloso - Drawing & Coloring Anime-Style Characters By Chyan\"
set "subsPath=%videoPath%EN SUBS\"

set "outputCSV=output.csv"

rem Create CSV header
echo "M4V File","SRT File" > "%outputCSV%"

rem Iterate through M4V files and find corresponding SRT files
for %%v in ("%videoPath%*.m4v") do (
    set "videoName=%%~nv"
    set "videoNumber=!videoName:~-2!"
    
    set "srtFile="
    for %%s in ("!videoNumber!") do (
        set "srtFile=!subsPath!sub%%~ns.srt"
    )
    
    echo "!videoName!","!srtFile!" >> "%outputCSV%"
)

echo "CSV file created: %outputCSV%"
