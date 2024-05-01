import shutil
import subprocess
import os
import time

blender_path = r"D:\\blender401\\blender.exe"
blend_file = r"D:\\job\\upload_assets\\model_lib\\your_blend_file.blend"

original_file_path = r"C:\\Users\\Admin\\source\\repos\\bpython_automation\\blenderkit_extra\\preprocessrenderpreview.py"
thumbnail_angles = ['DEFAULT', 'FRONT', 'SIDE','TOP' ]
#thumbnail_snap_tos = ['GROUND', 'WALL', 'CEILING', 'FLOAT']
thumbnail_snap_tos = ['GROUND']
def edit_thumbnail_properties(file_path, new_angle='DEFAULT', new_snap_to='GROUND'):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if "def set_thumbnail_properties(object_name, angle='DEFAULT', snap_to='GROUND'):" in line:
            # Find the line where the set_thumbnail_properties function is defined
            start_index = i + 1  # Start modifying from the next line
            end_index = start_index  # End modifying at the next function definition or the end of the file

            # Find the end of the function
            for j in range(start_index, len(lines)):
                if "def" in lines[j]:
                    end_index = j
                    break
            
            # Modify the angle and snap_to values
            for k in range(start_index, end_index):
                if "obj.blenderkit.thumbnail_angle" in lines[k]:
                    lines[k] = f"        obj.blenderkit.thumbnail_angle = '{new_angle}'\n"
                elif "obj.blenderkit.thumbnail_snap_to" in lines[k]:
                    lines[k] = f"        obj.blenderkit.thumbnail_snap_to = '{new_snap_to}'\n"

    # Write the modified lines to a new file
    new_file_path = file_path.replace('.py', f'_{new_angle}_{new_snap_to}.py')
    with open(new_file_path, 'w') as new_file:
        new_file.writelines(lines)

    return new_file_path



def process_all_blend_files(directory, script_file):
    # List all blend files in the directory
    blend_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.blend')]

    for blend_file in blend_files:
        print(f"Processing {blend_file}...")
        # Start Blender as a subprocess for each blend file
        process = subprocess.Popen([blender_path, blend_file, '--python' , script_file])
        time.sleep(40)

        #process.wait(180)

def create_and_move_files(directory, angle, snap_to):
    # Create folder name from angle and snap_to
    folder_name = f"{angle}_{snap_to}"
    folder_path = os.path.join(directory, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # Move JPG files to the created folder
    for file in os.listdir(directory):
        if file.lower().endswith('.jpg'):
            file_path = os.path.join(directory, file)
            shutil.move(file_path, os.path.join(folder_path, file))
# Example usage:
directory = r"D:\\job\\upload_assets\\model_lib"
for angle in thumbnail_angles:
            for snap_to in thumbnail_snap_tos:
                print(angle," ",snap_to )

                new_file_path = edit_thumbnail_properties(original_file_path, angle, snap_to)
                process_all_blend_files(directory, new_file_path)
                
                time.sleep(10)
                create_and_move_files(directory, angle, snap_to)
