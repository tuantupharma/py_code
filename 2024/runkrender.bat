@echo off

rem Define the path to Blender executable
set BLENDER_EXE=C:\blender\K-Cycles_2023_4.01\blender.exe

rem Define the path to the blend file
set BLEND_FILE=\\192.168.0.7\senshu\DATA\Natural_scene3\rendblend\Cam1_Camera.blend

rem Define the range of frames to render
set START_FRAME=101
set END_FRAME=200
set FRAME_BATCH_SIZE=10

rem Define the file name for the CSV file and its path
set CSV_FILE=S:\rendermanager\render\renderprogress.csv

rem Check if the CSV file exists, if not, generate it
if not exist %CSV_FILE% (
    call :generate_csv
) else (
    call :check_status
)

pause
exit /b

:generate_csv
echo Generating renderprogress.csv...
echo frame_start,frame_end,status >> %CSV_FILE%
for /L %%i in (%START_FRAME%,%FRAME_BATCH_SIZE%,%END_FRAME%) do (
    set /a FRAME_END=%%i+%FRAME_BATCH_SIZE%-1
    echo %%i,!FRAME_END!,pending>> %CSV_FILE%
)
echo CSV file created: %CSV_FILE%
exit /b

:check_status
rem Check if all status lines are "done"
set "ALL_DONE=true"
for /f "skip=1 tokens=3 delims=," %%a in (%CSV_FILE%) do (
    if "%%a" neq "done" set "ALL_DONE=false"
)

rem If all status lines are "done", prompt user for confirmation before deleting the CSV file and regenerate it
if "%ALL_DONE%"=="true" (
    echo All status lines are "done". Do you want to delete the CSV file and regenerate it? (Y/N)
    set /p DELETE_CONFIRM=
    if /i "%DELETE_CONFIRM%"=="Y" (
        del %CSV_FILE%
        call :generate_csv
    ) else (
        echo CSV file deletion canceled.
    )
) else (
    rem Loop through the frame ranges and render if status is "pending"
    echo checking for render...
    for /f "skip=1 tokens=1,2,3 delims=," %%i in (%CSV_FILE%) do (
        echo checkstatus before rendering
        
        if /I "%%k"=="pending" (
            echo Rendering frames %%i to %%j
            rem Mark status as "rendering"
            call :update_status "rendering" %%i %%j
            "%BLENDER_EXE%" -b "%BLEND_FILE%" -s %%i -e %%j -a
            rem Mark status as "done"
            call :update_status "done" %%i %%j
        )
    )
)
exit /b

:update_status
rem Update the status in the CSV file
(for /f "tokens=1,* delims=:" %%A in ('findstr /n "^" %CSV_FILE%') do (
    set "line=%%B"
    if "%%A"=="%~2" (
        set "line=!line:%~3,%~4,%~5=,%~3,%~4,%~5!"
    )
    echo(!line!
    echo(!line!>>%CSV_FILE%.tmp
)) > nul
move /y %CSV_FILE%.tmp %CSV_FILE% >nul
exit /b
