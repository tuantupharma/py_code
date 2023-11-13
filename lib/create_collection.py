import bpy

def create_and_move_to_collection(empty):
    # Get the name of the empty object
    empty_name = empty.name
    
    # Create a collection with the same name as the empty
    new_collection = bpy.data.collections.new(empty_name)
    bpy.context.scene.collection.children.link(new_collection)
    
    # Move the empty to the new collection
    new_collection.objects.link(empty)
    
    # Move children objects of the empty to the new collection
    for child in empty.children:
        new_collection.objects.link(child)

# Iterate through all empties in the scene
for obj in bpy.context.scene.objects:
    if obj.type == 'EMPTY':
        create_and_move_to_collection(obj)
