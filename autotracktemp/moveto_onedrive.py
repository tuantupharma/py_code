import csv
import subprocess
import os

def move_files_with_rclone(csv_file, rclone_path, destination):
    # Read filetogone.csv
    with open(csv_file, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        folder_path = r'C:\blender\blender_temp'
        for row in csv_reader:
            file_name = row['File Name']
            # Construct the full file path
            file_path = os.path.join(folder_path, file_name)
            # Use rclone to move the file to the destination
            rclone_cmd = f"{rclone_path} move \"{file_path}\" {destination}"
            subprocess.run(rclone_cmd, shell=True)

# Example usage:
csv_file = 'filetogone.csv'
rclone_path = r'I:\rclone-v1.65.1-windows-amd64\rclone.exe'
destination = 'rsync_htt:/tempblend'
move_files_with_rclone(csv_file, rclone_path, destination)
