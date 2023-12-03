import bpy

# Create a set to store external file paths
external_files = set()

# Iterate through all the materials in the current blend file
for material in bpy.data.materials:
    if material.node_tree:
        for node in material.node_tree.nodes:
            if node.type == 'TEX_IMAGE':
                image = node.image
                if image and image.source == 'FILE':
                    external_files.add(image.filepath)

# Print the list of external files
for file_path in external_files:
    print("External File:", file_path)
