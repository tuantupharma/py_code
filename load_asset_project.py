import bpy
import os
import shutil

# Function to check if a file exists in the new path
def file_exists(new_path):
    return os.path.exists(new_path)

# Read "miss.txt"
missed_files = []
with open("miss.txt", 'r') as file:
    missed_files = file.readlines()

# Specify the original and new paths
original_path = "d:\\job\\"
new_path = "\\\\192.168.0.7\\senshu\\JOBSTUDIO_2022\\"

# Process the missed files
for file_path in missed_files:
    file_path = file_path.strip()
    if original_path in file_path:
        new_file_path = file_path.replace(original_path, new_path)
        if file_exists(new_file_path):
            # Copy the file from the new path to the missing path
            shutil.copy(new_file_path, file_path)
            print(f"Copied {file_path} from {new_file_path}")
        else:
            print(f"File not found in NAS or NAS not connected: {new_file_path}")
    else:
        print(f"File path does not contain {original_path}: {file_path}")

# Display a message to save and reload the file
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
bpy.ops.wm.open_mainfile(filepath=bpy.data.filepath)

print("Files copied. Save and reload the file.")
