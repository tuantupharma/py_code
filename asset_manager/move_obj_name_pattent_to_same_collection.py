import bpy

def create_and_move_to_collection(obj, collection_name):
    # Create a collection with the specified name if it doesn't exist
    if collection_name not in bpy.data.collections:
        new_collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(new_collection)
    
    # Link the object to the collection
    bpy.data.collections[collection_name].objects.link(obj)

# Iterate through all objects in the scene
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        # Split the object name into parts based on "_" delimiter
        name_parts = obj.name.split("_")
        
        if len(name_parts) >= 3:
            object_name = name_parts[0]
            variant = name_parts[1]
            collection_name = f"{object_name}_{variant}"
            
            # Move the object to the appropriate collection
            create_and_move_to_collection(obj, collection_name)

            # Move children objects of the object to the same collection
            for child in obj.children:
                child_name_parts = child.name.split("_")
                if len(child_name_parts) >= 3 and child_name_parts[0] == object_name and child_name_parts[1] == variant:
                    create_and_move_to_collection(child, collection_name)
