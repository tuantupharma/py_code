import bpy
import os

# Get the name of the current Blender file
file_name = bpy.path.basename(bpy.data.filepath)
file_name_without_extension = os.path.splitext(file_name)[0]

# Create an asset catalog with the same name as the Blender file
asset_catalog_name = file_name_without_extension
if asset_catalog_name not in bpy.data.asset_studios:
    bpy.ops.asset.add_catalog(name=asset_catalog_name)

# Get the created asset catalog
asset_catalog = bpy.data.asset_studios[asset_catalog_name]

# Add all objects from the current Blender file to the asset catalog
for obj in bpy.data.objects:
    asset_catalog.add_object(obj)
