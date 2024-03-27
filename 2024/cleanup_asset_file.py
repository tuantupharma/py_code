import bpy
import os

def get_empty_by_name(empty_name):
    """
    Get an empty object by its name.

    Parameters:
        empty_name (str): The name of the empty object to find.

    Returns:
        bpy.types.Object: The empty object if found, None otherwise.
    """
    scene = bpy.context.scene
    for obj in scene.objects:
        if obj.type == 'EMPTY' and obj.name == empty_name:
            return obj
    return None


def link_collection_to_scene(collection_name):
    """
    Link a collection to the scene's collection.

    Parameters:
        collection_name (str): Name of the collection to be linked.

    Returns:
        bpy.types.Collection: Linked collection if found, None otherwise.
    """
    scene = bpy.context.scene
    collection = bpy.data.collections.get(collection_name)

    if collection:
        print(collection.name)
        # Link the collection to the scene's collection
        scene.collection.children.link(collection)
        return collection
    else:
        print(f"Collection '{collection_name}' not found.")
        return None
    
def get_collection_parent(file_collection):
  for parent_collection in bpy.data.collections:
    if file_collection.name in parent_collection.children.keys():
      parent_names= parent_collection.name
      print("parent_names" + parent_names)
      return parent_names
    
        
def get_collection_by_file_name():
    """
    Get the collection with the same name as the file name.

    Returns:
    - The collection with the same name as the file name.
    """
    # Get the file name without extension
    file_name = os.path.splitext(os.path.basename(bpy.data.filepath))[0]

    # Iterate through all collections and find the one with the same name as the file name
    for collection in bpy.data.collections:
        if collection.name == file_name:
            return collection

def remove_unused_collections():
    """
    Unlink all collections except the one with the same name as the file name.
    """
    # Get the collection with the same name as the file name
    file_collection = get_collection_by_file_name()
    
    if file_collection:
            parent_collection = get_collection_parent(file_collection)
            print(parent_collection) 
                
    # Unlink all other collections
            for collection in bpy.data.collections:
                if collection != file_collection and parent_collection and  collection.name != "Scene Collection"  and collection.name != parent_collection:
                    bpy.data.collections.remove(collection)
            rmcha = bpy.data.collections.get(parent_collection)

def remove_unused_objects():
    """
    Unlink all objects not belonging to the collection with the same name as the file name.
    """
    # Get the collection with the same name as the file name
    file_collection = get_collection_by_file_name()
    if file_collection:
        parent_collection = get_collection_parent(file_collection)
    # Unlink all objects not belonging to the file collection
        for obj in bpy.data.objects:
            if obj.users_collection  and  file_collection not in obj.users_collection :
                if obj != emptyname:                                                      
                    bpy.data.objects.remove(obj)
    

def save_file():

    bpy.types.BlendData.orphans_purge()
    """
    Save the Blender file.
    """
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)

# Remove all collections except the one with the same name as the file name
addcol = get_collection_by_file_name()
emptyname = get_empty_by_name(addcol.name)
remove_unused_collections()

# Remove all objects not belonging to the collection with the same name as the file name
remove_unused_objects()

#link_collection_to_scene(addcol.name)
# Save the Blender file
save_file()

