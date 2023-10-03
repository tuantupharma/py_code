import bpy
import random
from mathutils import Vector

# Clear the existing "random_props_instance" collection
if "random_props_instance" in bpy.data.collections:
    bpy.data.collections.remove(bpy.data.collections["random_props_instance"])

# Create a new "random_props_instance" collection
random_props_instance = bpy.data.collections.new("random_props_instance")
bpy.context.scene.collection.children.link(random_props_instance)

# Get references to the "box" and "boolbox" objects
box = bpy.data.objects.get("box")
boolbox = bpy.data.objects.get("boolbox")

if box is None:
    print("Error: 'box' object not found!")
    quit()

# Function to calculate the min and max coordinates based on vertices
def min_max_coordinates_from_vertices(vertices):
    min_coords = Vector((float('inf'), float('inf'), float('inf')))
    max_coords = Vector((-float('inf'), -float('inf'), -float('inf')))
    
    for vertex in vertices:
        min_coords.x = min(min_coords.x, vertex.x)
        min_coords.y = min(min_coords.y, vertex.y)
        min_coords.z = min(min_coords.z, vertex.z)
        max_coords.x = max(max_coords.x, vertex.x)
        max_coords.y = max(max_coords.y, vertex.y)
        max_coords.z = max(max_coords.z, vertex.z)
    
    return min_coords, max_coords

# Get the vertices of the "box" and "boolbox" objects
if box:
    box_vertices = [box.matrix_world @ Vector(v.co) for v in box.data.vertices]
    min_box, max_box = min_max_coordinates_from_vertices(box_vertices)
    print(f"Box Min Coordinates: {min_box}")
    print(f"Box Max Coordinates: {max_box}")
else:
    print("Error: 'box' object not found!")

if boolbox:
    boolbox_vertices = [boolbox.matrix_world @ Vector(v.co) for v in boolbox.data.vertices]
    min_boolbox, max_boolbox = min_max_coordinates_from_vertices(boolbox_vertices)
    print(f"Boolbox Min Coordinates: {min_boolbox}")
    print(f"Boolbox Max Coordinates: {max_boolbox}")
else:
    print("Boolbox not found in the scene.")

# Get the objects in the "random_props" collection
random_props_collection = bpy.data.collections.get("random_props")
if random_props_collection:
    random_props_objects = random_props_collection.objects
else:
    print("Error: 'random_props' collection not found!")
    quit()

# Create instances for each object in "random_props"
for obj in random_props_objects:
    # Define the number of instances for each object (20 instances per object)
    num_instances = 200

    # Define the range of positions (within the "box" boundaries)
    min_x, max_x = min_box.x, max_box.x
    min_y, max_y = min_box.y, max_box.y
    min_z, max_z = min_box.z, max_box.z
    
    #offset
    obj_offset = 0.14

    # Create a list to store used positions
    used_positions = []

    # Function to check if a position is inside the "boolbox" boundaries
    def is_position_inside_boolbox(position):
        if boolbox:
            return (
                min_boolbox.x <= position.x <= max_boolbox.x and
                min_boolbox.y <= position.y <= max_boolbox.y and
                min_boolbox.z <= position.z <= max_boolbox.z
            )
        else:
            return False

    # Create random instances within the specified limits for each object
    for _ in range(num_instances):
        # Attempt to generate a random position within the "box" boundaries
        attempts = 0
        while attempts < 100:  # Limit the number of attempts to avoid infinite loop
            x = random.uniform(min_x, max_x) + obj_offset
            y = random.uniform(min_y, max_y) + obj_offset
            z = random.uniform(min_z, max_z) 

            # Check if the position is inside the "boolbox" boundaries
            if is_position_inside_boolbox(Vector((x, y, z))):
                continue

            # Check if the position is already used
            position_key = (round(x, 2), round(y, 2), round(z, 2))  # Use rounded positions as keys
            if position_key not in used_positions:
                used_positions.append(position_key)
                break  # Valid position found, exit the loop

            attempts += 1

        if attempts >= 100:
            print("Warning: Unable to find a non-overlapping position, skipping instance creation.")
            continue

        # Choose a random object from the "random_props" collection
        random_obj = obj

        # Create an instance of the object and set its location
        instance = random_obj.copy()
        instance.data = random_obj.data.copy()
        instance.location = (x, y, z)

        # Link the instance to the "random_props_instance" collection
        random_props_instance.objects.link(instance)

print(f"Created instances for all objects in 'random_props' collection in 'random_props_instance' collection.")
