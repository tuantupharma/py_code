import bpy
import os

def process_blend_files(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".blend"):
            file_path = os.path.join(folder_path, file_name)
            process_blend_file(file_path)

def process_blend_file(file_path):
    # Load the blend file
    bpy.ops.wm.open_mainfile(filepath=file_path)

    # Get the current scene and its name
    scene = bpy.context.scene
    scene_name = scene.name

    # Check if a collection with the scene name exists
    if scene_name in bpy.data.collections:
        # Close the file if the collection already exists
        bpy.ops.wm.save_mainfile()        
    else:
        # Create a new collection with the scene name
        new_collection = bpy.data.collections.new(scene_name)
        bpy.context.scene.collection.children.link(new_collection)

        # Set the new collection as an asset
        new_collection.asset_mark()

        # Move all other collections into the new collection
        for collection in bpy.data.collections:
            if collection != new_collection:
                new_collection.children.link(collection)

        # Save the modified file
        bpy.ops.wm.save_mainfile()

        # Close the file


# Folder containing blend files
blend_files_folder = r'K:\\bkit_asset\\scenes'

# Process all blend files in the folder
process_blend_files(blend_files_folder)
