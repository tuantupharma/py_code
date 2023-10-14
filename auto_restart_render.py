import os
import time
import subprocess
import glob

blender_path = "C:\\Blender\\blender_3_6\\blender.exe"
blend_file = "I:\\job\\asset TVC\\Sneaker\\sneaker_cam2_t.blend"
render_folder = "i:\\job\\asset TVC\\zrender"
start_frame = 1
end_frame = 120

# Check for already rendered frames and skip them
existing_frames = [int(os.path.splitext(os.path.basename(png))[0]) for png in glob.glob(os.path.join(render_folder, '*.png'))]
for frame in existing_frames:
    if frame >= start_frame and frame <= end_frame:
        start_frame = frame + 1

# Start the initial Blender render
blender_command = [blender_path, "-b", blend_file, "-s", str(start_frame), "-e", str(end_frame), "-a"]
blender_process = subprocess.Popen(blender_command)

while True:
    time.sleep(5)  # Adjust the polling interval as needed

    if blender_process.poll() is not None:
        # Blender render process has finished
        # Step 1: Get the name of the latest PNG file in the folder
        latest_png = max(glob.glob(os.path.join(render_folder, '*.png')), key=os.path.getctime)

        # Step 2: Kill the Blender process
        blender_process.kill()

        # Step 3: Start Blender and render from the next frame
        frame_number = int(os.path.splitext(os.path.basename(latest_png))[0]) + 1
        if frame_number > end_frame:
            # All frames have been rendered
            print("All frames rendered. Exiting.")
            break
        blender_command = [blender_path, "-b", blend_file, "-s", str(frame_number), "-e", str(end_frame), "-o", os.path.join(render_folder, "image_####"), "-a"]
        blender_process = subprocess.Popen(blender_command)

    if not blender_process.poll() is None:
        # Blender process ended abruptly (for some reason)
        print("Blender process terminated unexpectedly. Exiting.")
        break
