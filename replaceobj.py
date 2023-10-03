import bpy

# Get a reference to the "Factory 13.001" collection
factory_collection = bpy.data.collections.get("factory 13.001")

if factory_collection:
    # Find the linked collection "Collection 2 Instance" in the current file
    linked_instance_collection = bpy.data.collections.get("Collection 2")

    if linked_instance_collection:
        # Create a list to store the empty objects to process
        empty_objects_to_process = [obj for obj in factory_collection.objects if obj.type == "EMPTY"]

        # Set the batch size (adjust as needed)
        batch_size = 10

        # Loop through the empty objects in batches
        while empty_objects_to_process:
            batch = empty_objects_to_process[:batch_size]
            empty_objects_to_process = empty_objects_to_process[batch_size:]

            for obj in batch:
                # Record the empty's transformation, including scale
                old_location = obj.location.copy()
                old_rotation_euler = obj.rotation_euler.copy()
                old_scale = obj.scale.copy()

                # Link an instance of "Collection 2 Instance" to the empty's location
                linked_instance = bpy.data.objects.new("Linked_Collection_2", None)
                linked_instance.instance_type = 'COLLECTION'
                linked_instance.instance_collection = linked_instance_collection
                linked_instance.location = old_location
                linked_instance.rotation_euler = old_rotation_euler
                linked_instance.scale = old_scale

                # Link the new instance to the "Factory 13.001" collection
                factory_collection.objects.link(linked_instance)

                # Remove the old empty
                bpy.data.objects.remove(obj)

        # Update the scene to reflect the changes
        bpy.context.view_layer.update()

        print("Linked collection 'Collection 2 Instance' replaced all empty objects in 'Factory 13.001' collection with scale preserved.")
    else:
        print("Linked collection 'Collection 2 Instance' not found in the current scene.")
else:
    print("Collection 'Factory 13.001' not found.")
