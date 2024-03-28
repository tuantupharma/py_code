import logging
import threading
import bpy
from bpy import context
import time
import os


def worker(event):
    while not event.isSet():
        logging.debug("worker thread checking in")
        event.wait(1)

def mainwatch():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(relativeCreated)6d %(threadName)s %(message)s"
    )
    event = threading.Event()

    thread = threading.Thread(target=worker, args=(event,))
    thread_two = threading.Thread(target=worker, args=(event,))
    thread.start()
    thread_two.start()

    while not event.isSet():
        try:
            logging.debug("Checking in from main thread")
            event.wait(0.75)
        except KeyboardInterrupt:
            event.set()
            break

def save_and_exit_blender():
    # Save the current Blender file
    bpy.ops.wm.save_mainfile()

    # Quit Blender
    bpy.ops.wm.quit_blender()

def select_empty_objects():
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Select empty objects
    for obj in bpy.context.scene.objects:
        if obj.type == 'EMPTY':
            obj.select_set(True)

def is_in_asset_collection(obj_name):
    # Get the collection by name
    collection = bpy.data.collections.get("Assets")

    # Check if the collection exists
    if collection is None:
        print("Error: Collection 'Assets' does not exist.")
        return False

    # Check if the object is in the collection
    for obj in collection.objects:
        if obj.name == obj_name:
            return True

    return False

def get_empty_names():
    # List to store empty names
    empty_names = ''

    # Iterate through all objects in the scene
    for obj in bpy.context.scene.objects:
        # Check if the object is an empty
        if obj.type == 'EMPTY' and is_in_asset_collection(obj.name):
            # Add the empty's name to the list
            empty_names = obj.name
            obj.select_set(True)

    return empty_names

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
            return  # Exit the function after selecting the first empty object found
    
    print("No empty objects found.")
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

def getcurrent3dviewport(context):
    
    for window in context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                print("scene loaded")
                bpy.data.window_managers["WinMan"].blenderkitUI.down_up = 'UPLOAD'
                get_empty_names()

event = threading.Event()
objectselect = get_empty_names()
print(objectselect)

x=1
time.sleep(1)
select_empty_object()
getcurrent3dviewport(context)


while x ==1:
    time.sleep(1)
    object = bpy.data.objects[objectselect].blenderkit
    if object:
        object.name = get_empty_names()
        bpy.context.object.blenderkit.thumbnail_use_gpu = True
        #bpy.context.object.blenderkit.thumbnail_angle = 'DEFAULT'
        #bpy.context.object.blenderkit.thumbnail_angle = 'FRONT'
        #bpy.context.object.blenderkit.thumbnail_angle = 'SIDE'
        #bpy.context.object.blenderkit.thumbnail_snap_to = 'GROUND'
        #bpy.context.object.blenderkit.thumbnail_snap_to = 'WALL'
        #bpy.context.object.blenderkit.thumbnail_snap_to = 'CEILING'
        #bpy.context.object.blenderkit.thumbnail_snap_to = 'FLOAT'
        bpy.context.object.blenderkit.thumbnail_resolution = '2048'
        bpy.context.object.blenderkit.thumbnail_denoising = True
        object.thumbnail_background_lightness = 0.5
        #render
        set_thumbnail_properties(object.name)
	
        time.sleep(6)
        x = 0
    else:
        x =1
        print("object not loaded")



save_and_exit_blender()

