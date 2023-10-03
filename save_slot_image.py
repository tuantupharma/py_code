import bpy

# Specify the output directory where the PNG images will be saved
output_directory = "D:\\job\\Scene_Room\\zRender\\room6"

# Set the file format to PNG
bpy.context.scene.render.image_settings.file_format = 'PNG'

# Loop through all render slots
for slot_index, render_slot in enumerate(bpy.context.scene.render.layers.active.slots):
    # Select the render slot
    bpy.context.scene.render.layers.active.active = slot_index

    # Specify the file name for the PNG image
    file_name = f"slot_{slot_index}.png"

    # Construct the full output path
    output_path = output_directory + file_name

    # Save the image
    bpy.data.images['Render Result'].save_render(output_path)

# Reset to the default render slot
bpy.context.scene.render.layers.active.active = 0

print("PNG images saved for each render slot.")
