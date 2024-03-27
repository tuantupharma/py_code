@echo off

rem Define the file name for the CSV file
set CSV_FILE=renderprogress.csv

rem Check if the CSV file already exists, if yes, delete it
if exist %CSV_FILE% del %CSV_FILE%

rem Write the header row to the CSV file
echo frame_start,frame_end,status >> %CSV_FILE%

rem Define the range of frames to render
set START_FRAME=1
set END_FRAME=200
set FRAME_BATCH_SIZE=10

rem Loop through the frames in batches of 10 and write the frame range and status to the CSV file
for /L %%i in (%START_FRAME%,%FRAME_BATCH_SIZE%,%END_FRAME%) do (
    rem Calculate frame end
    set /a FRAME_END=%%i+%FRAME_BATCH_SIZE%-1
    echo %%i, !FRAME_END!, pending >> %CSV_FILE%
)

echo CSV file created: %CD%\%CSV_FILE%
