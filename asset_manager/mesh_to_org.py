import bpy


# Deselect all objects
bpy.ops.object.select_all(action='DESELECT')
       
# Loop through all objects in the scene
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        obj.select_set(True)  # Select the mesh object 
        # Set the origin to the center of mass
       # bpy.context.view_layer.objects.active = obj
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
        
        # Move the object to (0, 0, 0)
        obj.location = (0, 0, 0)
        
    else:
        print("not move",obj.name)



