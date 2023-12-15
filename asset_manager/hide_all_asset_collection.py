import bpy

# Step 1: Loop through each collection and perform the desired actions
for collection in bpy.context.scene.collection.children:
    print("loop" ,collection.name) 
    if collection.library:
    # Disable the collection in the view layer
        bpy.context.view_layer.layer_collection.children[collection.name].exclude = True
        print("hide" ,collection.name)
    else:
         print("not" ,collection.name) 
         print("is ",collection.library)