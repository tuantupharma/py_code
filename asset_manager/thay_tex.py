import bpy
import os

texture_folder = "E:\\New folder\\kitbash_lib\\Kitbash3D - Mini Kit Post-Apocalypse\\KB3DTextures"

def find_matching_texture(texture_name):
    for filename in os.listdir(texture_folder):
        if texture_name in filename:
            return os.path.join(texture_folder, filename)
    return None

def update_texture_node(node, texture_name):
    label = node.label.lower()
    
    if label == "base color":
        suffix = "_Diff"
    elif label == "roundness":
        suffix = "_Gloss"
    elif "diff" in label:
        suffix = "_Diff"
    elif "disp" in label:
        suffix = "_Disp"
    elif "gloss" in label:
        suffix = "_Gloss"
    elif "nor" in label:
        suffix = "_Nor"
    elif "spec" in label:
        suffix = "_Spec"
    else:
        return False
    
    texture_path = find_matching_texture(material_name + suffix)
    if texture_path:   
            node.image = bpy.data.images.load(texture_path)
            return True
        
            
    return False

# Loop through all materials
for material in bpy.data.materials:
    material_name = material.name
    if material.name == "Dots Stroke":
        continue  # Skip the "Dots Stroke" material
    # Loop through all image texture nodes in the material
    for node in material.node_tree.nodes:
        if node.type == 'TEX_IMAGE' and node.name.startswith("Image Texture."):
            
                texture_name = node.image.name
                if material_name in texture_name:
                    continue
                else:
                 if update_texture_node(node, material_name):
                        print(f"Updated texture for node {node.name} in material {material.name}")

print("Texture updates completed.")
