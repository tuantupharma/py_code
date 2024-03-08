import bpy
import os


def get_obj_name():
    # Get the active object
    active_object = bpy.context.active_object

    # Check if there is an active object
    if active_object is not None:
        # Get the name of the active object
        object_name = active_object.name
        print("The name of the active object is:", object_name)
        return object_name
    else:
        print("No object is currently selected.")

def set_displace_modifier_texture(texture_name):
    selected_object = bpy.context.active_object
    for modifier in selected_object.modifiers:
        if modifier.type == 'DISPLACE':
            displace_modifier = modifier
            break

    if displace_modifier is not None:
    # Set the texture for the Displace modifier
        displace_modifier.texture = bpy.data.textures.get(texture_name)
        print(f"Texture '{texture_name}' set for the Displace modifier.")
    else:
        print("Selected object does not have a Displace modifier.")
    




def add_subsurface():
    objName = get_obj_name()
    bpy.ops.object.modifier_add(type='SUBSURF')
    #bpy.data.object.modifiers["Subdivition"].subdivition_type
    bpy.data.objects[objName].modifiers["Subdivision"].levels =3
    bpy.data.objects[objName].modifiers["Subdivision"].render_levels =3
    #=====
    bpy.ops.object.modifier_add(type='DISPLACE')
    #bpy.data.objects[objName].modifiers["Displace"].Direction = "Normal"
    set_displace_modifier_texture("Texture.001")
    bpy.data.objects[objName].modifiers["Displace"].texture_coords = 'UV'
    bpy.data.objects[objName].modifiers["Displace"].direction = 'NORMAL'
    bpy.data.objects[objName].modifiers["Displace"].strength = 0.050
    bpy.data.objects[objName].modifiers["Displace"].mid_level = 0.500


    bpy.ops.object.modifier_add(type='SMOOTH')
    bpy.data.objects[objName].modifiers["Smooth"].use_x = True
    bpy.data.objects[objName].modifiers["Smooth"].use_y = True        
    bpy.data.objects[objName].modifiers["Smooth"].use_z = True
    bpy.data.objects[objName].modifiers["Smooth"].iterations = 2

    bpy.ops.object.modifier_add(type='WAVE')
    bpy.data.objects[objName].modifiers["Wave"].use_normal = True
    bpy.data.objects[objName].modifiers["Wave"].height = 0.1
    bpy.data.objects[objName].modifiers["Wave"].width = 1
    bpy.data.objects[objName].modifiers["Wave"].narrowness = 1
    bpy.data.objects[objName].modifiers["Wave"].speed = 0.05
    texture_name = "Texture.002"
    bpy.data.objects[objName].modifiers["Wave"].texture = bpy.data.textures.get(texture_name)