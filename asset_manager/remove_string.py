import bpy

def clean_object_name(name):
    return name.replace("Desirefx.me_", "")

# Iterate through all objects in the scene
for obj in bpy.context.scene.objects:
    # Clean the object name
    obj.name = clean_object_name(obj.name)
    
    # Clean the mesh name for mesh objects
    if obj.type == 'MESH':
        obj.data.name = clean_object_name(obj.data.name)