import bpy
import math
def create_empty(name, location=(0, 0, 0)):
    """
    Create an empty object in the scene or return an existing one with the specified name.

    Args:
    - name: Name of the empty object.
    - location: Location of the empty object (default is (0, 0, 0)).
    """
    existing_empty = bpy.data.objects.get(name)
    if existing_empty:
        existing_empty.location = location
        return existing_empty
    else:
        bpy.ops.object.empty_add(location=location)
        empty = bpy.context.object
        empty.name = name
        empty.empty_display_size = 0.5  # Adjust display size if needed
        return empty

def is_zero_vector(vector):
    """
    Checks if the given vector has all components as zero.

    Parameters:
        vector (tuple): Vector coordinates (x, y, z).

    Returns:
        bool: True if all components are zero, False otherwise.
    """
    return all(math.isclose(component, 0) for component in vector)


def group_objects_with_empty(objects, empty):
    """
    Group a list of objects with an empty object.

    Args:
    - objects: List of Blender objects to be grouped.
    - empty: Empty object to use for grouping.
    """
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = empty
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

def organize_objects_with_empty_by_collection(collection):
    """
    Organize objects in a collection by grouping them with an empty object.

    Args:
    - collection: Blender collection containing objects to be organized.
    """
    lowest_z_xyz = (0,0,0)
    if not collection.children:  # Check if the collection has no child collections
        lowest_z_value = float('inf')
        for obj in collection.objects:
            if obj.type == 'MESH':
                if is_zero_vector(obj.location):
                      continue
                if obj.location.z < lowest_z_value :
                    
                    lowest_z_value = obj.location.z
                    lowest_z_xyz = obj.location.xyz  # Store XYZ coordinates of the object with the lowest Z value
        empty = create_empty(f"{collection.name}", lowest_z_xyz)  # Pass XYZ coordinates to create_empty

        for obj in collection.objects:
            if obj.type == 'MESH':
                group_objects_with_empty([obj], empty)

def organize_objects_in_all_children_collections(parent_collection_name):
    """
    Recursively organize objects in all children collections within a parent collection.

    Args:
    - parent_collection_name: Name of the parent collection.
    """
    parent_collection = bpy.data.collections.get(parent_collection_name)
    if parent_collection:
        for child_collection in parent_collection.children:
            organize_objects_with_empty_by_collection(child_collection)
            organize_objects_in_all_children_collections(child_collection.name)

# Example usage:
# Organize objects in all children collections within the "Assets" collection
organize_objects_in_all_children_collections("Assets")


# Move all created empty objects to the origin (0, 0, 0)
for obj in bpy.data.objects:
    
    if obj.type == 'EMPTY' and not obj.parent:
        obj.location = (0, 0, 0)