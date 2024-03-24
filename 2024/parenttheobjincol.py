import bpy

def set_parent(collection_name, parent_name, parent_collection_name):
    """
    Sets the parent of objects within a collection to another object and moves them to a specified collection.

    Parameters:
        collection_name (str): Name of the collection containing the objects to be parented.
        parent_name (str): Name of the object to be set as the parent.
        parent_collection_name (str): Name of the collection to which the objects will be moved.
    """
    collection = bpy.data.collections.get(collection_name)
    parent = bpy.data.objects.get(parent_name)
    parent_collection = bpy.data.collections.get(parent_collection_name)
    
    if collection and parent and parent_collection:
        for obj in collection.objects:
            obj.parent = parent
            
            
    else:
        print("One or more of the specified objects or collections do not exist.")

# Usage
parent_collection = parent_collection = bpy.data.collections.get('Assets')
for col in parent_collection.children:
    set_parent(col.name, col.name, "Assets")
    print("done " + col.name)