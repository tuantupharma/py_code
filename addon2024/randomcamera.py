import bpy
import random

def create_camera_frames(frame_range, object_name):
    for frame in range(frame_range[0], frame_range[1]+1):
        bpy.context.scene.frame_set(frame)
        
        # Create a new camera
        bpy.ops.object.camera_add(location=(random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-1, 10)))
        new_camera = bpy.context.object
        
        # Set camera rotation
        new_camera.rotation_euler = (random.uniform(0, 2 * 3.14159), random.uniform(0, 2 * 3.14159), random.uniform(0, 2 * 3.14159))
        
        # Track camera to the object
        bpy.context.view_layer.objects.active = new_camera
        bpy.ops.object.constraint_add(type='TRACK_TO')
        bpy.context.object.constraints["Track To"].target = bpy.data.objects[object_name]
        print("new cam is set")
        
        # Make a copy of the camera
        bpy.ops.object.duplicate(linked=False)
        print("new cam is set")
        # Reset the active object to the original camera
        bpy.context.view_layer.objects.active = bpy.data.objects[object_name]
        
create_camera_frames((1, 250), "objtrack")