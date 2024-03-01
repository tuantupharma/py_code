import os
import csv

def save_mp4_paths_to_csv(root_folder, csv_filename):
    # Open CSV file for writing
    with open(csv_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['MP4 File Path'])

        # Walk through each subdirectory
        for root, dirs, files in os.walk(root_folder):
            for file in files:
                # Check if file is an mp4 file
                if file.endswith('.mp4'):
                    mp4_path = os.path.join(root, file)
                    csv_writer.writerow([mp4_path])

# Example usage
root_folder = r'F:\downloi\Twinmotion 2023 Essentials for All Basic to Pro'
csv_filename = 'mp4file.csv'
save_mp4_paths_to_csv(root_folder, csv_filename)
