import subprocess
import os
import time

blender_path = r"D:\\blender401\\blender.exe"

def process_all_blend_files(directory, script_file):
    # List all blend files in the directory
    blend_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.blend')]

    for blend_file in blend_files:
        print(f"Processing {blend_file}...")
        
        # Start Blender as a subprocess for each blend file
        process = subprocess.Popen([blender_path, blend_file, '--python' , script_file])

        # Wait for Blender to fully load
        time.sleep(30)  # Adjust the wait time as needed
        
        # Wait for the subprocess to finish
        process.wait()

# Example usage:
directory = r"D:\\job\\upload_assets\\model_lib"
script_file = r"C:\\Users\Admin\source\\repos\bpython_automation\\blenderkit_extra\\preprocessrenderpreview.py"

process_all_blend_files(directory, script_file)
