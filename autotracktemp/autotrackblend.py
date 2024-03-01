import os
import csv
from datetime import datetime

def track_blend_files(folder_path, csv_filename):
    # Initialize a list to store file information
    files_info = []

    # Iterate over files in the folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Check if the file has a .blend, .blend1, or .blend2 extension
            if file.endswith('.blend') or file.endswith('.blend1') or file.endswith('.blend2'):
                file_path = os.path.join(root, file)
                # Get the last modified time of the file
                mod_time = os.path.getmtime(file_path)
                # Convert timestamp to a readable date format
                mod_time_formatted = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
                # Append file name and last modified date to the list
                files_info.append([file, mod_time_formatted])

    # Write file information to a CSV file
    with open(csv_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write header
        csv_writer.writerow(['File Name', 'Last Modified Date'])
        # Write file information
        csv_writer.writerows(files_info)

# Example usage:
folder_path = r'C:\blender\blender_temp'
csv_filename = 'trackingtemp.csv'
track_blend_files(folder_path, csv_filename)
