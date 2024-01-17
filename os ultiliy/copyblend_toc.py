import os
import shutil

def get_blend_files(folder_path):
    blend_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.blend'):
                blend_files.append(os.path.join(root, file))
    return blend_files

def copy_blend_files(source_folder, destination_folder):
    log_entries = []

    for blend_file in get_blend_files(source_folder):
        file_name, file_extension = os.path.splitext(os.path.basename(blend_file))
        destination_file = os.path.join(destination_folder, f"{file_name}{file_extension}")

        # Check if the destination file already exists
        counter = 1
        while os.path.exists(destination_file):
            destination_file = os.path.join(destination_folder, f"{file_name}_copy{counter}{file_extension}")
            counter += 1

        shutil.copy2(blend_file, destination_file)
        log_entries.append((blend_file, destination_file))

    return log_entries

def write_log(log_entries, log_file_path):
    with open(log_file_path, 'w', encoding='utf-8-sig') as log_file:
        log_file.write("Original Name,New Name\n")
        for entry in log_entries:
            log_file.write(f"{entry[0]},{entry[1]}\n")


# Folder containing blend files
source_folder = r'C:\\Blender\\lib_addon\\addons\\Vegetation\data\\vegetation'

# Destination folder for copied blend files
destination_folder = r'K:\\tmpb'

# Log file path
log_file_path = r'K:\\tmpb\\log.csv'

# Copy blend files and log the changes
log_entries = copy_blend_files(source_folder, destination_folder)

# Write log to a CSV file
write_log(log_entries, log_file_path)

print("Blend files copied successfully.")
