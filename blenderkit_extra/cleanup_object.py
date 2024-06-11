import bpy
import csv
import os

def read_csv_and_process(filename='bk_object.csv'):
    # Get the directory of the current Blender file
    blend_file_dir = os.path.dirname(bpy.path.abspath("//"))

    # Construct the full path for the CSV file in the same directory
    csv_file_path = os.path.join(blend_file_dir, filename)

    # Open and read the CSV file
    with open(csv_file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Check if the 'Type of Object' is 'MESH'
            if row['Type of Object'] == 'MESH':
                obj_name = row['Name of Object']
                obj = bpy.data.objects.get(obj_name)
                
                if obj is not None:
                    try:
                        # Move the cursor to the object's location
                        bpy.context.scene.cursor.location = obj.location

                        # Create a new plane object at the cursor location
                        bpy.ops.mesh.primitive_plane_add(size=1)
                        plane = bpy.context.active_object

                        # Remove the mesh data from the plane to use it as an empty
                        plane.data = None

                        # Copy rotation and scale to the plane
                        plane.rotation_euler = obj.rotation_euler
                        plane.scale = obj.scale

                        # Link the mesh data of the object to the plane
                        plane.data = obj.data

                        # Rename the mesh data to match the object name
                        if obj.data:
                            obj.data.name = obj_name

                        # Rename the plane to indicate it contains the mesh data
                        plane.name = f"Empty_{obj_name}"

                        print(f"Processed object: {obj_name}")
                    except TypeError as e:
                        print(f"Error processing object {obj_name}: {e}")
                        continue

# Example usage
read_csv_and_process()
