import os
import shutil

base_path = r'D:\job\mela\solid'

# Function to move files from folders named "check" to their parent folder
def move_files_from_check_folders(base_path):
    # Iterate through all directories in the base path
    for root, dirs, files in os.walk(base_path):
        for directory in dirs:
            if directory == 'check':
                check_folder_path = os.path.join(root, directory)
                parent_folder = os.path.dirname(check_folder_path)
                # Iterate through files in the "check" folder and move them to the parent folder
                for file in os.listdir(check_folder_path):
                    file_path = os.path.join(check_folder_path, file)
                    shutil.move(file_path, parent_folder)
                # Remove the now-empty "check" folder
                os.rmdir(check_folder_path)
                print(f"All files from {check_folder_path} moved to {parent_folder} and folder removed.")

# Call the function with the base path
move_files_from_check_folders(base_path)
