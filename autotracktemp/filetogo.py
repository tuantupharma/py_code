import csv
import os
from datetime import datetime, timedelta

def find_old_files(tracking_file, output_file):
    files_to_delete = []

    # Calculate the datetime 24 hours ago
    twenty_four_hours_ago = datetime.now() - timedelta(hours=24)

    with open(tracking_file, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            file_name = row['File Name']
            mod_time_str = row['Last Modified Date']
            mod_time = datetime.strptime(mod_time_str, '%Y-%m-%d %H:%M:%S')
            # Check if the file was modified over 24 hours ago
            if mod_time < twenty_four_hours_ago:
                files_to_delete.append([file_name, mod_time_str])

    # Write old files information to a new CSV file
    with open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write header
        csv_writer.writerow(['File Name', 'Last Modified Date'])
        # Write file information
        csv_writer.writerows(files_to_delete)

# Example usage:
tracking_file = 'trackingtemp.csv'
output_file = 'filetogone.csv'
find_old_files(tracking_file, output_file)
