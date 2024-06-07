import bpy

def animate_camera_to_vertices():
    # Get the object named "campos"
    try:
        obj = bpy.data.objects['campos']
    except KeyError:
        print("Object 'campos' not found")
        return
    
    # Check if the object is a mesh and has vertices
    if obj.type != 'MESH' or len(obj.data.vertices) == 0:
        print("Object 'campos' is not a mesh or has no vertices")
        return

    # Get the active camera
    active_camera = bpy.context.scene.camera
    if not active_camera:
        print("No active camera found")
        return

    # Animate the camera to move to each vertex position
    for frame_number, vertex in enumerate(obj.data.vertices, start=1):
        # Get the world position of the vertex
        world_pos = obj.matrix_world @ vertex.co
        
        # Set the camera location to the vertex position
        active_camera.location = world_pos

        # Insert keyframes for location
        active_camera.keyframe_insert(data_path="location", frame=frame_number)

        # Optionally set the end frame of the scene to the last keyframe
        bpy.context.scene.frame_end = frame_number

# Run the function
animate_camera_to_vertices()