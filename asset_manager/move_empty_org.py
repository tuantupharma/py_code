import bpy

# Loop through all objects in the scene
for obj in bpy.context.scene.objects:
    if obj.type == 'EMPTY':
        obj.location = (0, 0, 0)

print("Empty objects moved to (0, 0, 0).")
