import bpy

# Step 1: Loop through each collection and perform the desired actions
for collection in bpy.context.scene.collection.children:
    # Select all objects in the collection
    bpy.ops.object.select_all(action='DESELECT')
    for obj in collection.all_objects:
        obj.select_set(True)
    
    
    # Move the selected objects to (0, 0, 0)
    bpy.ops.transform.translate(value=(-obj.location.x, -obj.location.y, -obj.location.z))

    # Disable the collection in the view layer
    bpy.context.view_layer.layer_collection.children[collection.name].exclude = True
