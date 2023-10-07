import bpy

# Get the current active view layer
active_view_layer = bpy.context.view_layer

# Iterate through all collections in the file
for collection in bpy.data.collections:
    # Check if the collection contains any objects
    if collection.objects:
        # Iterate through objects in the collection
        for obj in collection.objects:
            # Check if the object is an armature with library overrides
            if obj.type == 'ARMATURE' and obj.library:
                # Check if the object is in the current active view layer
                if obj.name in active_view_layer.objects:
                    # Check if the object is visible in the view layer
                    if not obj.hide_viewport:
                        # Select the object in the Outliner
                        obj_name = obj.name  # Replace with the name of your object
                        obj = bpy.data.objects.get(obj_name)

                        # Check if the object exists
                        if obj  is not None:
                              # Select the object
                              obj.select_set(True)

                        # Resync the hierarchy of the selected object with library override
                        bpy.ops.object.mode_set(mode = 'OBJECT') #force object mode
                        bpy.ops.outliner.liboverride_troubleshoot_operation(
                            type='OVERRIDE_LIBRARY_RESYNC_HIERARCHY',
                            selection_set='SELECTED'
                        )

                        # Deselect the object after the operation
                        obj.select_set(False)

                        print(f"Resynced armature with library override: {obj.name}")
