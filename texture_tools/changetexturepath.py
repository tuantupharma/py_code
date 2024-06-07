import bpy
import os

def replace_textures():
    # Iterate over all images in the Blender data
    for img in bpy.data.images:
        if img.filepath.lower().endswith('.png'):
            # Get the base name of the file without the extension
            base_name = os.path.splitext(img.filepath)[0]
            
            # Construct the DDS file path
            dds_filepath = base_name + '.dds'
            
            # Check if the corresponding DDS file exists
            if os.path.isfile(bpy.path.abspath(dds_filepath)):
                print(f"Replacing {img.filepath} with {dds_filepath}")
                
                # Replace the image's filepath with the DDS one
                img.filepath = bpy.path.relpath(dds_filepath)
                
                # Reload the image to apply changes
                img.reload()
            else:
                print(f"DDS file not found for {img.filepath}")

# Run the function
replace_textures()
