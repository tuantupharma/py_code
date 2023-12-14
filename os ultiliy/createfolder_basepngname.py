import os

def get_png_files(folder_path):
    # Get the names of all PNG files in the folder
    png_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.png')]
    return png_files

def create_folders(png_files, base_folder):
    # Create folders based on the names of PNG files
    for png_file in png_files:
        folder_name = os.path.splitext(png_file)[0]  # Remove the '.png' extension
        folder_path = os.path.join(base_folder, folder_name)

        # Check if the folder already exists before creating it
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder created: {folder_path}")
        else:
            print(f"Folder already exists: {folder_path}")

# Example usage
folder_path = "C:\\Blender\\lib_addon\\Jungle_Scapes"
base_folder = "C:\\Blender\\lib_addon\\namefolder"
png_files = get_png_files(folder_path)

if png_files:
    create_folders(png_files, base_folder)
else:
    print("No PNG files found in the specified folder.")
