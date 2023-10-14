SetTitleMatchMode, 2 ; Allow flexible window title matching
#IfWinActive, Blender

; Send the keyboard shortcuts to trigger the operation
Send, ^O ; Press Ctrl+O to open the file menu
Sleep 1000 ; Wait for the menu to open (adjust the delay as needed)

Send, e ; Press 'e' to open the External Data menu
Sleep 500 ; Wait for the submenu to open (adjust the delay as needed)

Send, r ; Press 'r' to run the Report Missing Files operation
Sleep 1000 ; Wait for the operation to complete (adjust the delay as needed)

; You can add more code here to read the report or perform other tasks

#IfWinActive ; Reset the window title matching mode
