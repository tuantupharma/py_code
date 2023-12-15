import bpy
import os

def update_catalog_names(blender_file_path):
    # Set the catalog file path in the same directory as the Blender file
    catalog_file_path = os.path.join(os.path.dirname(blender_file_path), "blender_assets.cats.txt")

    # Check if the catalog file exists
    if not os.path.isfile(catalog_file_path):
        print(f"Error: Catalog file not found at {catalog_file_path}. Aborting script.")
        return

    # Read the collection names from the collection_names.txt file
    collection_names_file_path = os.path.join(os.path.dirname(blender_file_path), "collection_names.txt")

    # Check if the collection names file exists
    if not os.path.isfile(collection_names_file_path):
        print(f"Error: Collection names file not found at {collection_names_file_path}. Aborting script.")
        return

    with open(collection_names_file_path, 'r') as collection_names_file:
        collection_names = [line.strip() for line in collection_names_file.readlines()]

    # Open the Asset Catalog Definition file for reading and updating
    with open(catalog_file_path, 'r') as catalog_file:
        catalog_lines = catalog_file.readlines()

    # Update lines in the catalog file
    for index, line in enumerate(catalog_lines):
        if line.startswith('#') or line.startswith('VERSION'):
            # Ignore comments and the version line
            continue

        # Split the line into UUID, Catalog Path, and Simple Catalog Name
        line_parts = line.strip().split(':')

        if len(line_parts) == 3:
            uuid, _, _ = line_parts
        else:
            # Handle the case where the line doesn't have enough values to unpack
            print(f"Error parsing line {index + 1} in the catalog file. Skipping...")
            continue

        # Update the line in the catalog file
        catalog_lines[index] = f"{uuid}:{collection_names[index % len(collection_names)]}:{collection_names[index % len(collection_names)]}\n"

    # Open the Asset Catalog Definition file for writing and update the content
    with open(catalog_file_path, 'w') as catalog_file:
        catalog_file.writelines(catalog_lines)

# Get the path of the current Blender file
blender_file_path = bpy.data.filepath

# Ensure the Blender file has been saved before running the script
if blender_file_path:
    # Call the function to update catalog names
    update_catalog_names(blender_file_path)

    print(f"Catalog names updated in blender_assets.cats.txt")
else:
    print("Please save the Blender file before running the script.")
