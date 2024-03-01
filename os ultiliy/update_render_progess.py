import os
import csv

def find_missing_png_sequence(folder_path, csv_file_path):
    # Get the list of all PNG files in the folder
    all_files = [f.lower() for f in os.listdir(folder_path) if f.lower().endswith('.png')]

    # Check for missing files in the sequence
    missing_files = []
    for i in range(len(all_files)):
        expected_file = f"{i+1:04d}.png"
        if expected_file not in all_files:
            missing_files.append(expected_file)

    # Save the missing files to CSV
    with open(csv_file_path, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["Missing PNG Files"])
        csv_writer.writerows([[file] for file in missing_files])

    return missing_files

if __name__ == "__main__":
    folder_path = r"T:\Thang_2_2024\Isometric\Render\Shot2"
    csv_file_path = "update.csv"

    if os.path.exists(csv_file_path):
        # If CSV file exists, check and update the missing files
        existing_missing_files = []
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                existing_missing_files.append(row[0])

        missing_files = find_missing_png_sequence(folder_path, csv_file_path)

        # Check if previously missing files are still missing
        still_missing_files = [file for file in existing_missing_files if file.lower() in missing_files]

        if still_missing_files:
            print("The following files are still missing:")
            for file in still_missing_files:
                print(file)
        else:
            print("No missing files from the previous run.")
    else:
        # If CSV file doesn't exist, find missing files and create CSV
        find_missing_png_sequence(folder_path, csv_file_path)
        print(f"CSV file '{csv_file_path}' created successfully.")
