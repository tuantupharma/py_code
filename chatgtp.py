import bpy
import random

# Get the currently active object
active_object = bpy.context.active_object

# Number of objects to create
num_objects = 60

# Spacing between objects
spacing = 1.0

# Loop to create and position linked objects
for i in range(num_objects):
    # Duplicate the active object
    new_object = active_object.copy()
    new_object.data = active_object.data.copy()
    bpy.context.collection.objects.link(new_object)
    
    # Set the location of the new object along the -y axis
    new_location = active_object.location.copy()
    new_location.y -= i * spacing
    new_object.location = new_location
    
    # Random rotation along the z-axis
    z_rotation = random.uniform(0, 2 * 3.14159)  # Random rotation between 0 and 2*pi
    new_object.rotation_euler.z = z_rotation

# Select all newly created objects
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.context.collection.objects:
    obj.select_set(True)

# Update the scene to reflect the changes
bpy.context.view_layer.update()
