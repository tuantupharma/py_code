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
    num_instances = 220

    # Define the range of positions (within the "box" boundaries)
    min_x, max_x = min_box.x, max_box.x
    min_y, max_y = min_box.y, max_box.y
    min_z, max_z = min_box.z, max_box.z

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
        # Generate random positions within the "box" boundaries
        x = random.uniform(min_x, max_x)
        y = random.uniform(min_y, max_y)
        z = random.uniform(min_z, max_z)
        
        # Check if the position is inside the "boolbox" boundaries
        if is_position_inside_boolbox(Vector((x, y, z))):
            continue
        
        # Create an instance of the object and set its location
        instance = obj.copy()
        instance.data = obj.data.copy()
        instance.location = (x, y, z)
        
        # Link the instance to the "random_props_instance" collection
        random_props_instance.objects.link(instance)

print(f"Created instances for all objects in 'random_props' collection in 'random_props_instance' collection.")
