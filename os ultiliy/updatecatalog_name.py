import bpy
import os

def update_catalog_names(catalog_file_path):
    # Open the Asset Catalog Definition file for reading
    with open(catalog_file_path, 'r') as catalog_file:
        catalog_lines = catalog_file.readlines()

    # Get all collections in the current Blender file
    collections = bpy.data.collections

    # Iterate through collection lines in the Asset Catalog Definition file
    for index, line in enumerate(catalog_lines):
        if line.startswith('#') or line.startswith('VERSION'):
            # Ignore comments and the version line
            continue

        # Split the line into UUID, Catalog Path, and Simple Catalog Name
        uuid, catalog_path, _ = line.strip().split(':')

        # Find the corresponding collection by name
        matching_collection = next((collection for collection in collections if collection.name == catalog_path), None)

        # If a matching collection is found, update the Simple Catalog Name in the catalog file
        if matching_collection:
            catalog_lines[index] = f"{uuid}:{catalog_path}:{matching_collection.name}\n"

    # Open the Asset Catalog Definition file for writing and update the content
    with open(catalog_file_path, 'w') as catalog_file:
        catalog_file.writelines(catalog_lines)

# Get the path of the current Blender file
blender_file_path = bpy.data.filepath

# Ensure the Blender file has been saved before running the script
if blender_file_path:
    # Set the catalog file path in the same directory as the Blender file
    catalog_file_path = os.path.join(os.path.dirname(blender_file_path), "blender_assets.cats.txt")

    # Call the function to update catalog names
    update_catalog_names(catalog_file_path)

    print(f"Catalog names updated in {catalog_file_path}")
else:
    print("Please save the Blender file before running the script.")
