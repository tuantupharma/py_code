@echo off

rem Define the file name for the CSV file and its path
set CSV_FILE=renderprogress.csv

rem Define the line number and column number to retrieve
set LINE_NUMBER=3
set COLUMN_NUMBER=3

rem Check if the CSV file exists
if exist %CSV_FILE% (
    rem Read the value of the specified column in the specified line
    for /f "usebackq tokens=%COLUMN_NUMBER% delims=," %%i in (`type "%CSV_FILE%" ^| findstr /n "^" ^| findstr "^%LINE_NUMBER%:"`) do (
        echo Value at line %LINE_NUMBER%, column %COLUMN_NUMBER%: %%i
    )
) else (
    echo CSV file does not exist.
)

pause
