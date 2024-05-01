import bpy
from bpy import context
import time
import sys

def set_thumbnail_properties(object_name, angle='DEFAULT', snap_to='GROUND'):
    obj = bpy.data.objects.get(object_name)
    print(obj)
    
    if obj:
        bpy.ops.object.kill_bg_process(process_type='THUMBNAILER', process_source='MODEL')
        
        obj.blenderkit.thumbnail_angle = angle
        obj.blenderkit.thumbnail_snap_to = snap_to
        obj.blenderkit.thumbnail_use_gpu = True
        obj.blenderkit.thumbnail_resolution = '2048'
        obj.blenderkit.thumbnail_denoising = True
        #if obj.thumbnail_background_lightness:
        #    obj.thumbnail_background_lightness = 0.5

        bpy.ops.object.blenderkit_generate_thumbnail()
        time.sleep(1)


def save_and_exit_blender():
    # Save the current Blender file
    bpy.ops.wm.save_mainfile()

    # Quit Blender
    bpy.ops.wm.quit_blender()

def select_empty_object():
    # Deselect all objects first
    bpy.ops.object.select_all(action='DESELECT')
    
    # Iterate through all objects in the scene
    for obj in bpy.context.scene.objects:
        # Check if the object is an empty
        if obj.type == 'EMPTY':
            # Select the empty object
            obj.select_set(True)
            # Update the 3D viewport
            bpy.context.view_layer.objects.active = obj
            return obj.name  # Return the name of the selected empty object
    
    print("No empty objects found.")
    return None


def getcurrent3dviewport(context):
    for window in context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                print("Scene loaded")
                bpy.data.window_managers["WinMan"].blenderkitUI.down_up = 'UPLOAD'
                select_empty_object()

def main():

    # Trigger to get the 3D viewport
    getcurrent3dviewport(context)

    # Set thumbnail properties and render preview
    empty_object_name = select_empty_object()
    if empty_object_name:
        set_thumbnail_properties(empty_object_name)
        

        save_and_exit_blender()
    else:
        print("Error: Empty object not found.")

# Run the main function if the script is run directly
if __name__ == "__main__":  
    main() 
