import bpy
import random
import math

# Function to apply random rotation to an object within specified ranges
def random_rotate_object(obj, min_x, max_x, min_z, max_z):
    obj.rotation_euler.x = math.radians(random.uniform(min_x, max_x))
    obj.rotation_euler.y = math.radians(random.uniform(-360, 360))  # Total random for Y
    obj.rotation_euler.z = math.radians(random.uniform(min_z, max_z))

# Define rotation ranges (in degrees)
min_x_rotation = 60
max_x_rotation = 133
min_z_rotation = -40
max_z_rotation = 40

# Get the selected objects
selected_objects = bpy.context.selected_objects

# Check if there are selected objects
if selected_objects:
    # Iterate through selected objects and apply random rotations
    for obj in selected_objects:
        random_rotate_object(obj, min_x_rotation, max_x_rotation, min_z_rotation, max_z_rotation)
    print(f"Random rotations applied to selected objects:\n"
          f"X-axis: {min_x_rotation}° to {max_x_rotation}°\n"
          f"Y-axis: Total random\n"
          f"Z-axis: {min_z_rotation}° to {max_z_rotation}°")
else:
    print("No objects are selected.")
