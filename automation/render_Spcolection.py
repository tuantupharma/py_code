import bpy
import os

# Set the output folder for rendered images
output_folder = r'D:\\job\\gumi\\Gumitaquan2401\\zrender\\'

# Get the active scene
scene = bpy.context.scene

# Set the collection name
collection_name = "SP"

# Find the collection by name
collection = bpy.data.collections.get(collection_name)

if collection:
    # Check if all objects in the collection are set to not render
    if all(obj.hide_render for obj in collection.objects):
        for obj in collection.objects:
            # Enable render for the current object
            obj.hide_render = False

            # Set the output path for the current object
            output_path = os.path.join(output_folder, f"trans_{obj.name}.png")
            bpy.context.scene.render.filepath = output_path
            bpy.context.scene.render.image_settings.file_format = 'PNG'

            # Set other rendering settings as needed

            # Render image
            bpy.ops.render.render(write_still=True)

            print(f"Rendered {obj.name} to {output_path}")

            # Disable render for the current object
            obj.hide_render = True

    else:
        print("Disabling render for all objects in the collection.")
        for obj in collection.objects:
            obj.hide_render = True
else:
    print(f"Collection {collection_name} not found.")
