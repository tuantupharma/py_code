py autotrackblend.py

if exist "trackingtemp.csv" (
    echo "len danh sach file up"
    py filetogo.py
) else (
    echo File not found
)
if exist "filetogone.csv" (
    echo "upload files"
    
    py moveto_onedrive.py
) else (
    echo File not found
)

if exist "trackingtemp.csv" (
    del "trackingtemp.csv"
    echo File deleted
)

if exist "filetogone.csv" (
    del "filetogone.csv"
    echo File deleted
)
