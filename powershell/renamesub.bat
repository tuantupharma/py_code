@echo off
setlocal enabledelayedexpansion

set "csvFile=output.csv"
set "folderPath=C:\Users\Admin\source\repos\bpython_automation\powershell\sun"

rem Skip header and iterate through each line in the CSV
for /f "skip=1 tokens=1,2 delims=," %%a in (%csvFile%) do (
    set "videoName=%%a"
    set "srtPath=%%b"
    
    rem Extract the numeric suffix from the SRT file name
    for /f "tokens=1,* delims=_" %%c in ("!srtPath!") do set "suffix=%%d"
    
    rem Construct the new SRT file name based on the video name
    set "newSrtName=!videoName!!suffix!"
    
    rem Rename the SRT file
    ren "!srtPath!" "!newSrtName!"
    
    echo Renamed: !srtPath! to !newSrtName!
)

echo "Renaming complete."
