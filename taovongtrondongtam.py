import bpy
import math

# Number of concentric circles
num_circles = 5

# Radius of the largest circle
radius = 1.0

# Number of vertices per concentric circle
vertices_per_circle = 32  # Adjust as needed

# Radius of the small circles
small_circle_radius = 0.05  # Adjust as needed

# Create a new collection to hold the circles
collection_name = "ConcentricCircles"
if collection_name not in bpy.data.collections:
    collection = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(collection)

# Create the concentric circles with small circles
for i in range(num_circles):
    circle_radius = radius * (i + 1) / num_circles
    
    # Calculate the angle increment based on the desired number of vertices
    angle_increment = 2 * math.pi / vertices_per_circle
    
    for j in range(vertices_per_circle):
        angle = j * angle_increment
        x = circle_radius * math.cos(angle)
        y = circle_radius * math.sin(angle)
        z = 0.0  # Adjust the Z-coordinate if needed
        
        # Create a small circle object
        bpy.ops.mesh.primitive_circle_add(vertices=vertices_per_circle, radius=small_circle_radius, fill_type='NGON', location=(x, y, z))
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
bpy.context.object.name = "ConcentricCircles"

# Select and set the active object
bpy.context.view_layer.objects.active = bpy.context.object
bpy.context.object.select_set(True)
