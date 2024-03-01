import os
import csv
import shutil

def copy_srt_files_to_mp4_folder(csv_filename, source_folder):
    # Open CSV file for reading
    with open(csv_filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip header row

        # Iterate through each row in the CSV
        for row in csv_reader:
            mp4_path = row[0]
            mp4_filename = os.path.basename(mp4_path)
            mp4_name, _ = os.path.splitext(mp4_filename)
            srt_filename = mp4_name + '.srt'
            srt_source_path = os.path.join(source_folder, srt_filename)
            mp4_folder = os.path.dirname(mp4_path)
            srt_destination_path = os.path.join(mp4_folder, srt_filename)
            
            # Check if the SRT file exists in the source folder
            if os.path.exists(srt_source_path):
                shutil.copy2(srt_source_path, srt_destination_path)
                print(f"Copied {srt_filename} to {mp4_folder}")
            else:
                print(f"SRT file {srt_filename} not found in {source_folder}")

# Example usage
csv_filename = 'mp4file.csv'
source_folder = r'F:\downloi\Twinmotion 2023 Essentials for All Basic to Pro\vsub'
copy_srt_files_to_mp4_folder(csv_filename, source_folder)
