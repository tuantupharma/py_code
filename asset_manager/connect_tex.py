import bpy

def setup_material_texture(material, texture_type, texture_path):
    # Create an image texture node
    texture_node = material.node_tree.nodes.new(type='ShaderNodeTexImage')
    texture_node.location = (0, 300)
    texture_node.image = bpy.data.images.load(texture_path)
    
    if texture_type in ['_normal', '_specular', '_glossiness', '_height', '_Disp', '_Spec', '_gloss']:
        texture_node.color_space = 'NONE'  # Set Non-Color for specific textures
        
    # Connect the texture node based on texture type
    if texture_type == '_glossiness' or texture_type == '_gloss':
        invert_node = material.node_tree.nodes.new(type='ShaderNodeInvert')
        invert_node.location = (200, 300)
        material.node_tree.links.new(invert_node.outputs['Color'], texture_node.outputs['Color'])
        material.node_tree.links.new(material.node_tree.nodes['Principled BSDF'].inputs['Roughness'], invert_node.outputs['Color'])
    elif texture_type == '_normal':
        normal_map_node = material.node_tree.nodes.new(type='ShaderNodeNormalMap')
        normal_map_node.location = (200, 300)
        material.node_tree.links.new(normal_map_node.inputs['Color'], texture_node.outputs['Color'])
        material.node_tree.links.new(material.node_tree.nodes['Principled BSDF'].inputs['Normal'], normal_map_node.outputs['Normal'])
    else:
        material.node_tree.links.new(material.node_tree.nodes['Principled BSDF'].inputs['Base Color'], texture_node.outputs['Color'])
    
    return texture_node

# Specify the prefixes, suffixes, and texture directory
prefixes = ['KB3D_', 'KB3D_WZT_']
suffixes = ['_normal', '_specular', '_glossiness', '_height', '_Disp', '_Spec', '_gloss']
texture_directory = 'E:\KB3DTextures'

# Iterate through all materials
for material in bpy.data.materials:
    for prefix in prefixes:
        if material.name.startswith(prefix):
            material_name = material.name[len(prefix):]  # Extract material name without prefix
            for suffix in suffixes:
                texture_name = prefix + material_name + suffix
                texture_path = texture_directory + texture_name + '.png'  # Adjust the file format if needed
                if bpy.path.exists(texture_path):
                    texture_type = suffix
                    texture_node = setup_material_texture(material, texture_type, texture_path)
                    print(f"Connected '{texture_name}' to material '{material.name}'")

# Save the updated materials
for material in bpy.data.materials:
    if material.node_tree:
        material.node_tree.update_tag()
        material.use_nodes = True
        bpy.context.view_layer.objects.active = None  # Deselect the active object
        bpy.context.view_layer.objects.active = bpy.context.view_layer.objects.active  # Reselect the active object to refresh nodes
