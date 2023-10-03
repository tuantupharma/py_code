import bpy

# Define the name of the linked collection
linked_collection_name = "tamtonsat"

# Get a reference to the linked collection
linked_collection = bpy.data.collections.get(linked_collection_name)

if linked_collection:
    # Loop through all collections in the current file
    for collection in bpy.data.collections:
        # Check if the collection contains objects
        if collection.objects:
            # Loop through all objects in the collection
            for obj in collection.objects:
                # Check if the object is empty and its name matches the pattern
                if obj.type == "EMPTY" and obj.name.startswith("tamton+sat."):
                    # Record the empty's transformation, including scale
                    old_location = obj.location.copy()
                    old_rotation_euler = obj.rotation_euler.copy()
                    old_scale = obj.scale.copy()

                    # Link an instance of the linked collection to the empty's location
                    linked_instance = bpy.data.objects.new("Linked_" + linked_collection_name, None)
                    linked_instance.instance_type = 'COLLECTION'
                    linked_instance.instance_collection = linked_collection
                    linked_instance.location = old_location
                    linked_instance.rotation_euler = old_rotation_euler
                    linked_instance.scale = old_scale

                    # Link the new instance to the collection containing the empty
                    collection.objects.link(linked_instance)

                    # Remove the old empty
                    bpy.data.objects.remove(obj)

    # Update the scene to reflect the changes
    bpy.context.view_layer.update()

    print(f"Linked collection '{linked_collection_name}' replaced all matching empty objects.")
else:
    print(f"Linked collection '{linked_collection_name}' not found in the current scene.")
