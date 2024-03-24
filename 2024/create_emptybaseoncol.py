import bpy

# Get the "Assets" collection
assets_collection = bpy.data.collections.get("Assets")

print(assets_collection.name)
print("-------")
# Check if the "Assets" collection exists
if assets_collection:
    # Iterate through each child collection
    for child_collection in assets_collection.children:
        # Get the name of the child collection
        child_collection_name = child_collection.name
        print(child_collection_name)
        
        # Create the empty for the child collection
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        empty = bpy.context.object
        empty.name = child_collection_name
        mothercoll = empty.users_collection[0].name
        if mothercoll != "Assets":
            bpy.data.collections[mothercoll].objects.unlink(empty)
            bpy.data.collections["Assets"].objects.link(empty)
        
        
        

        