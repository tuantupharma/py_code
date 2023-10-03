import os
import bpy

# Directory containing subfolders with .blend files
root_directory = 'D:\\job\\datat9\\bkit\\assets\\scenes'

# Function to render a Blender file and save the image
def render_blend_file(blend_file):
    # Check if an image with the same name already exists
    image_file = bpy.path.display_name_from_filepath(blend_file) + '.png'
    if os.path.exists(image_file):
        print(f"Image '{image_file}' already exists. Skipping rendering.")
        return
    
    # Load the .blend file
    bpy.ops.wm.open_mainfile(filepath=blend_file)
    
    # Set output path and file format
    output_path = os.path.dirname(blend_file)
    bpy.context.scene.render.filepath = os.path.join(output_path, bpy.path.display_name_from_filepath(blend_file))
    
    # Render the image
    bpy.ops.render.render(write_still=True)

# Recursively search for .blend files in subfolders
for root, dirs, files in os.walk(root_directory):
    for file in files:
        if file.endswith('.blend'):
            blend_file = os.path.join(root, file)
            # Check if a .blend1 file with the same name exists
            blend1_file = blend_file + '1'
            if os.path.exists(blend1_file):
                render_blend_file(blend_file)

# Quit Blender (optional, you can remove this if you want to keep Blender open)
bpy.ops.wm.quit_blender()
