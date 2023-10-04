import bpy

# Specify the output directory where the rendered images will be saved
output_directory = "I://job//blenderkit_new//zrender//"

# Set the file format to PNG
bpy.context.scene.render.image_settings.file_format = 'PNG'

# Get a list of all collections starting with "Scene 1."
scene_collections = [collection for collection in bpy.data.collections if collection.name.startswith("Scene 1.")]

for idx, collection in enumerate(scene_collections):
    # Activate the current collection
    bpy.context.view_layer.layer_collection.children[idx].exclude = False

    # Render the image
    bpy.ops.render.render(write_still=True)

    # Specify the file name for the PNG image
    file_name = f"Scene_1_{idx}.png"

    # Construct the full output path
    output_path = output_directory + file_name

    # Save the image
    bpy.data.images['Render Result'].save_render(output_path)

    # Disable the current collection
    bpy.context.view_layer.layer_collection.children[idx].exclude = True

# Reset the view layer to the original state (all collections excluded)
for collection in bpy.data.collections:
    collection.exclude = True

print("Rendered images saved for each 'Scene 1.' collection.")
