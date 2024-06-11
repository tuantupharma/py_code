import bpy
import csv
import os

def list_blenderkit_objects():
    # Initialize an empty list to store objects with the 'blenderkit' custom property
    blenderkit_objects = []

    # Iterate through all objects in the current Blender scene
    for obj in bpy.data.objects:
        # Check if the object has the 'blenderkit' custom property
        if 'blenderkit' in obj.keys():
            # Add the object to the list
            blenderkit_objects.append(obj)

    # Return the list of objects with the 'blenderkit' custom property
    return blenderkit_objects

def write_objects_to_csv(objects, filename='bk_object.csv'):
    # Get the directory of the current Blender file
    blend_file_dir = os.path.dirname(bpy.path.abspath("//"))

    # Construct the full path for the CSV file in the same directory
    csv_file_path = os.path.join(blend_file_dir, filename)

    # Open the CSV file for writing
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(['Name of Object', 'Type of Object', 'Object Parent', 'Object Collection'])

        # Write data rows
        for obj in objects:
            name = obj.name
            obj_type = obj.type
            parent = obj.parent.name if obj.parent else 'None'
            collection_names = ', '.join([col.name for col in obj.users_collection])
            writer.writerow([name, obj_type, parent, collection_names])

# Example usage
blenderkit_objs = list_blenderkit_objects()
write_objects_to_csv(blenderkit_objs)

print(f'CSV file "bk_object.csv" created with {len(blenderkit_objs)} objects in the same folder as the Blender file.')
