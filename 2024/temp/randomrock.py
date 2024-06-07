import bpy
import random
from math import radians

def random_rotate_objects(collection_name):
    # Collect all objects with names containing 'rock' in the current scene
    rock_objects = [obj for obj in bpy.context.scene.objects if collection_name in obj.name]
    
    # Iterate through each object and perform random rotation on z axis
    for obj in rock_objects:
        angle_in_degrees = random.uniform(0, 360)
        angle_in_radians = radians(angle_in_degrees)
        
        # Apply the random rotations to z axis of the object
        obj.rotation_euler[2] = angle_in_radians
    
    print("Random rotation applied on objects with 'rock' in their name.")

# Calling function and passing collection name "rock"
random_rotate_objects('rock')
