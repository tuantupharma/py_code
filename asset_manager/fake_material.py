import bpy

# Name of the source material to copy from
source_material_name = "assetA"

# Loop through all materials in the scene
for material in bpy.data.materials:
    # Check if the material has nodes and is not the source material
    if material.use_nodes and material.name != source_material_name:
        nodes = material.node_tree.nodes
        
        # Check if the Principled BSDF shader is present and has no connections
        if 'Principled BSDF' not in nodes:
            continue
        
        principled_node = nodes['Principled BSDF']
        
        if not principled_node.inputs['Base Color'].is_linked:
            # Get the source material
            source_material = bpy.data.materials.get(source_material_name)
            
            if source_material:
                # Create a copy of the source material
                new_material = source_material.copy()
                new_material.name = material.name  # Keep the original material name
                
                # Remove the ".001" suffix from the new material's name
                if new_material.name.endswith(".001"):
                    new_material.name = new_material.name[:-4]
                
                # Replace the original material with the new copy
                material.user_remap(new_material)
                bpy.data.materials.remove(material)

print("Materials replaced if necessary.")
