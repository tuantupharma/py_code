def set_thumbnail_properties(object_name,angle,snap_to ):
    thumbnail_angles = ['DEFAULT', 'FRONT', 'SIDE']
    thumbnail_snap_tos = ['GROUND', 'WALL', 'CEILING', 'FLOAT']

    for angle in thumbnail_angles:
        for snap_to in thumbnail_snap_tos:
            # Select the object
            #bpy.data.objects[object_name].select_set(True)
            #bpy.context.view_layer.objects.active = bpy.data.objects[object_name]

            # Set thumbnail angle
            bpy.context.object.blenderkit.thumbnail_angle = angle
            
            # Set thumbnail snap to
            bpy.context.object.blenderkit.thumbnail_snap_to = snap_to
            
            bpy.context.object.blenderkit.thumbnail_use_gpu = True           
            bpy.context.object.blenderkit.thumbnail_resolution = '2048'
            bpy.context.object.blenderkit.thumbnail_denoising = True
            object.thumbnail_background_lightness = 0.5

            bpy.ops.object.blenderkit_generate_thumbnail()
            os.wait(30)
            
            time.sleep(1)
            print(angle)
            print(snap_to)
            # Deselect the object
            #bpy.data.objects[object_name].select_set(False)