# Set the path to the directory containing the SRT files
$directoryPath = "C:\Users\Admin\source\repos\bpython_automation\powershell\sun"

# Load the CSV file containing the new names
$csvPath = "C:\Users\Admin\source\repos\bpython_automation\powershell\sun\output.csv"
$newNames = Import-Csv $csvPath | Select-Object -ExpandProperty NewName

# Get all SRT files in the directory
$srtFiles = Get-ChildItem -Path $directoryPath -Filter *.srt

# Iterate through each SRT file and rename it based on the new names in the CSV
foreach ($srtFile in $srtFiles) {
    # Extract the current episode number from the file name (assuming the format is "Chyan_02.srt")
    $episodeNumber = [regex]::Match($srtFile.BaseName, '\d+').Value

    # Construct the new name based on the episode number and the new name from the CSV
    $newName = "$episodeNumber.srt"
    
    # Check if the file should be renamed
    if ($newNames -contains $newName) {
        $newFilePath = Join-Path -Path $directoryPath -ChildPath $newName
        Rename-Item -Path $srtFile.FullName -NewName $newName -Force
        Write-Host "Renamed: $($srtFile.Name) to $newName"
    } else {
        Write-Host "New name not found for $($srtFile.Name)"
    }
}

Write-Host "Script completed."
