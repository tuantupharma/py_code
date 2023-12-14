import bpy
import os

def export_collection_names():
    # Get the path of the current Blender file
    blend_file_path = bpy.data.filepath

    # Check if the Blender file has been saved
    if blend_file_path:
        # Set the output file path to be in the same directory as the Blender file
        output_file_path = os.path.join(os.path.dirname(blend_file_path), "collection_names.txt")

        # Get all collections in the scene
        collections = bpy.data.collections

        # Open the output file in write mode
        with open(output_file_path, 'w') as file:
            # Write the collection names to the file
            for collection in collections:
                file.write(collection.name + '\n')

        print(f"Collection names exported to {output_file_path}")
    else:
        print("Please save the Blender file before running the script.")

# Call the function to export collection names
export_collection_names()
