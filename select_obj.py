import bpy

# Get a reference to the object you want to select by its name
obj_name = "Cube"  # Replace with the name of your object
obj = bpy.data.objects.get(obj_name)

# Check if the object exists
if obj is not None:
    # Select the object
    obj.select_set(True)
