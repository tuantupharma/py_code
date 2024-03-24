import bpy
import math

def is_zero_vector(vector):
    """
    Checks if the given vector has all components as zero.

    Parameters:
        vector (tuple): Vector coordinates (x, y, z).

    Returns:
        bool: True if all components are zero, False otherwise.
    """
    return all(math.isclose(component, 0) for component in vector)


def get_lowest_point(collection_name):
    """
    Returns the coordinates (xyz) of the object with the lowest z value in the given collection.

    Parameters:
        collection_name (str): Name of the collection containing the objects.

    Returns:
        tuple: XYZ coordinates (x, y, z) of the lowest point.
    """
    collection = bpy.data.collections.get(collection_name)
    
    if not collection:
        print(f"Collection '{collection_name}' not found.")
        return None
    
    lowest_point = None
    lowest_z = float('inf')  # Initialize lowest z value to positive infinity
    
    for obj in collection.objects:
        if is_zero_vector(obj.location):
            continue
        
        if obj.location.z < lowest_z:
            lowest_z = obj.location.z
            lowest_point = obj.location
    
    return lowest_point

# Usage example
collection_name = "tulanh_style"
lowest_point = get_lowest_point(collection_name)
if lowest_point:
    print(f"The lowest point in collection '{collection_name}' is at coordinates: {lowest_point}")
else:
    print("No valid objects found in the collection.")
