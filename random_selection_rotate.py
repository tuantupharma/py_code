import bpy
import random
import math

# Function to apply random rotation to an object
def random_rotate_object(obj):
    obj.rotation_euler.x = random.uniform(0, 2 * math.pi)
    obj.rotation_euler.y = random.uniform(0, 2 * math.pi)
    obj.rotation_euler.z = random.uniform(0, 2 * math.pi)

# Get the selected objects
selected_objects = bpy.context.selected_objects

# Check if there are selected objects
if selected_objects:
    # Iterate through selected objects and apply random rotation
    for obj in selected_objects:
        random_rotate_object(obj)
    print("Random rotation applied to selected objects.")
else:
    print("No objects are selected.")
