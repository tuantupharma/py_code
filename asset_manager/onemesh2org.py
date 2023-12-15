import bpy

# Specify the name of the object you want to move its mesh origin
object_name = "Cube"  # Replace with the actual object name

# Get the object by name
obj = bpy.data.objects.get(object_name)

if obj and obj.type == 'MESH':
    # Store the object's current location
    original_location = obj.location.copy()
    
    # Move the object to the world origin
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
    bpy.ops.object.location_clear()
    
    # Restore the object's original location
    obj.location = original_location
else:
    print(f"Object '{object_name}' either does not exist or is not a mesh object.")
