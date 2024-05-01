import bpy

def clear_parent_transform():
    scene = bpy.context.scene
    for obj in scene.objects:
        if obj.parent is not None:
            # Store original parent and parent inverse matrix
            obj["original_parent"] = obj.parent
            obj["original_parent_inverse"] = obj.matrix_parent_inverse.copy()
            
            # Clear parent
            obj.parent = None


def rebind_original_parent(collection_name, parent_name, parent_collection_name):
    scene = bpy.context.scene
    collection = bpy.data.collections.get(collection_name)
    parent = bpy.data.objects.get(parent_name)
    parent_collection = bpy.data.collections.get(parent_collection_name)
    
    if collection and parent and parent_collection:
        for obj in collection.objects:
            obj.parent = parent
            
            
    else:
        print("One or more of the specified objects or collections do not exist.")

clear_parent_transform()
parent_collection = bpy.data.collections.get('Assets')
for col in parent_collection.children:
    rebind_original_parent(col.name, col.name,"Assets")
