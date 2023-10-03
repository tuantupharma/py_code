import bpy

# Get references to the collections
collection_soya = bpy.data.collections.get("soya")
collection_caphe = bpy.data.collections.get("caphe")

# Check if both collections exist
if collection_soya and collection_caphe:
    # Ensure both collections have the same number of objects
    if len(collection_soya.objects) == len(collection_caphe.objects):
        # Iterate through objects in both collections and copy transforms
        for obj_soya, obj_caphe in zip(collection_soya.objects, collection_caphe.objects):
            obj_caphe.location = obj_soya.location
            obj_caphe.rotation_euler = obj_soya.rotation_euler
            obj_caphe.scale = obj_soya.scale
        print("Transforms copied successfully.")
    else:
        print("Both collections must have the same number of objects.")
else:
    print("One or both collections do not exist.")
