import bpy
import os
import time

currentfilepath = os.path.dirname(bpy.data.filepath)
print(currentfilepath)


def select_objects_with_substring(substring):
    # Deselect all objects initially
    bpy.ops.object.select_all(action='DESELECT')

    # Loop through all objects in the scene
    for obj in bpy.context.scene.objects:
        
        # Check if the object's name contains the substring
        if substring in obj.name:
            # Select the object
            print("object selected.",obj.name )
            return   obj.select_set(True)
            
            
def switch_to_edit_mode_and_add_sphere():
    # Get the active object
    
    obj = bpy.context.active_object
    time.sleep(1)
    
    # Check if there's an active object
    if obj:
        # Switch to edit mode
        bpy.ops.object.mode_set(mode='EDIT')
        time.sleep(5)
        # Select all vertices
        bpy.ops.mesh.select_all(action='SELECT')
        time.sleep(1)
        # Delete all vertices
        bpy.ops.mesh.delete(type='VERT')

        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, location=(0, 0, 0))
        # Switch back to object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # Add a UV Sphere mesh
        
        
        print("Switched to edit mode, deleted all vertices, and added a sphere mesh.")
    else:
        print("No active object selected.")
        

# Construct the path to the vfxlib.blend file
vfxlib_blend_path = os.path.join(currentfilepath, "vfxlib.blend")
print(vfxlib_blend_path)
if os.path.exists(vfxlib_blend_path):
        print("vfxlib.blend file exists.")
        blendfile = vfxlib_blend_path  # Replace with the actual file path
        section = "\\Object\\"
        object = "bublle01"  # Replace with the name of the object you want to link
# Link the object from the other file to the current scene

        filepath  = blendfile + section + object
        directory = blendfile + section
        filename  = object

        bpy.ops.wm.append(
            filepath=filepath, 
            filename=filename,
            directory=directory)
    
        # Call the function
        select_objects_with_substring("bublle01")
        switch_to_edit_mode_and_add_sphere()
else:
        print("vfxlib.blend file does not exist.")
        
    




    
    
    