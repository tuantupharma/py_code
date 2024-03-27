@echo off
setlocal enabledelayedexpansion

rem Define the file name for the CSV file and its path
set CSV_FILE=renderprogress.csv

rem Define the line number and column number to update
set LINE_NUMBER=5
set COLUMN_NUMBER=3
set NEW_VALUE=hello

rem Check if the CSV file exists
if not exist "%CSV_FILE%" (
    echo Error: CSV file does not exist.
    exit /b 1
)

rem Validate line and column numbers
if %LINE_NUMBER% leq 0 (
    echo Error: Invalid line number.
    exit /b 1
)
if %COLUMN_NUMBER% leq 0 (
    echo Error: Invalid column number.
    exit /b 1
)

rem Update the value in the CSV file
set "line_index=1"
(for /f "tokens=* delims=" %%A in ('type "%CSV_FILE%"') do (
    if !line_index! equ %LINE_NUMBER% (
        set "line=%%A"
        set "new_line="
        set "col_index=1"
        for %%B in (!line!) do (
            if !col_index! equ %COLUMN_NUMBER% (
                set "new_line=!new_line!!NEW_VALUE!,"
            ) else (
                set "new_line=!new_line!%%B,"
            )
            set /a "col_index+=1"
        )
        echo !new_line:~0,-1!
    ) else (
        echo %%A
    )
    set /a "line_index+=1"
)) > %CSV_FILE%.tmp

rem Move the temporary file to replace the original CSV file
move /y %CSV_FILE%.tmp %CSV_FILE% >nul

echo Value at line %LINE_NUMBER%, column %COLUMN_NUMBER% updated to: %NEW_VALUE%
exit /b 0
