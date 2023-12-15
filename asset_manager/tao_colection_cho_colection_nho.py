import bpy

def create_and_move_to_collection(obj, collection_name):
    # Create a collection with the specified name if it doesn't exist
    if collection_name not in bpy.data.collections:
        new_collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(new_collection)
    
    # Link the object to the collection
    bpy.data.collections[collection_name].objects.link(obj)

# Get the "Components_grp" collection
components_grp_collection = bpy.data.collections.get("Components_grp")

if components_grp_collection:
    # Iterate through objects in the "Components_grp" collection
    for obj in components_grp_collection.objects:
        collection_name = obj.name
        
        # Move the object to its corresponding collection
        create_and_move_to_collection(obj, collection_name)
        
        # Move children objects of the object to the same collection
        for child in obj.children:
            create_and_move_to_collection(child, collection_name)
