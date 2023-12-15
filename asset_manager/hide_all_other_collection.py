import bpy

# Step 1: Loop through each collection and perform the desired actions
for collection in bpy.context.scene.collection.children:
    if collection.name != "Collection":
        bpy.context.view_layer.layer_collection.children[collection.name].exclude = True
        print("is ",collection.library)