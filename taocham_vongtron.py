import bpy
import math

# Number of small circles (points) to create
num_circles = 12

# Radius of the circle
circle_radius = 3.0

# Radius of the small circles
small_circle_radius = 0.1

# Create a new collection to hold the small circles
collection_name = "SmallCircles"
if collection_name not in bpy.data.collections:
    collection = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(collection)

# Calculate the angle increment for each small circle
angle_increment = 2 * math.pi / num_circles

# Create the small circles
for i in range(num_circles):
    angle = i * angle_increment
    x = circle_radius * math.cos(angle)
    y = circle_radius * math.sin(angle)
    z = 0.0  # Adjust the Z-coordinate if needed
    
    # Create a small circle object
    bpy.ops.mesh.primitive_circle_add(vertices=32, radius=small_circle_radius, fill_type='NGON', location=(x, y, z))
    small_circle = bpy.context.object
    
    # Link the small circle to the collection
    collection.objects.link(small_circle)

# Deselect all objects
bpy.ops.object.select_all(action='DESELECT')

# Select all small circle objects
for obj in bpy.data.objects:
    if obj.type == 'MESH' and obj.name.startswith("Circle"):
        obj.select_set(True)

# Join all small circles into one object
bpy.ops.object.join()

# Rename the joined object
bpy.context.object.name = "SmallCircles"

# Select and set the active object
bpy.context.view_layer.objects.active = bpy.context.object
bpy.context.object.select_set(True)
