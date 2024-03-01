import os
import csv
import shutil

def copy_mp4_files_from_csv(csv_filename, destination_folder):
    # Create destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Open CSV file for reading
    with open(csv_filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip header row
        
        # Copy each mp4 file to destination folder
        for row in csv_reader:
            mp4_path = row[0]
            mp4_filename = os.path.basename(mp4_path)
            destination_path = os.path.join(destination_folder, mp4_filename)
            shutil.copy2(mp4_path, destination_path)
            print(f"Copied {mp4_filename} to {destination_path}")

# Example usage
csv_filename = 'mp4file.csv'
destination_folder = r'F:\downloi\Twinmotion 2023 Essentials for All Basic to Pro\vsub'
copy_mp4_files_from_csv(csv_filename, destination_folder)
