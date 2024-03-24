import bpy
import csv
import os
import shutil

def clone_blend_file(blend_file_path, output_dir):
    """
    Clone a Blender file to the specified output directory.

    Args:
    - blend_file_path: Path to the Blender file to clone.
    - output_dir: Directory to clone the Blender file to.
    """
    shutil.copy2(blend_file_path, output_dir)

def main():
    # Get the path of the current blend file
    blend_file_path = bpy.data.filepath

    # Get the directory of the blend file
    blend_file_dir = os.path.dirname(blend_file_path)

    # Define the path to the CSV file
    csv_file_path = os.path.join(blend_file_dir, "tenfile.csv")

    # Check if the CSV file exists
    if not os.path.isfile(csv_file_path):
        print("CSV file 'tenfile.csv' not found")
        return

    # Define the output directory
    output_base_dir = "D:\\job\\upload_assets\\model_lib"

    # Read collection names from the CSV file
    with open(csv_file_path, mode='r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            collection_name = row[0]
            output_dir = os.path.join(output_base_dir, collection_name) + ".blend"

            # Clone the blend file to the output directory
            clone_blend_file(blend_file_path, output_dir)

            print(f"Blend file cloned to '{output_dir}'")

if __name__ == "__main__":
    main()
