import os
import subprocess
import glob
import logging
import tkinter as tk
from tkinter import filedialog

# Initialize the GUI
root = tk.Tk()
root.title("Blender Render GUI")

# Initialize variables for user input
render_folder = tk.StringVar()
blend_file = tk.StringVar()
start_frame = tk.IntVar()
end_frame = tk.IntVar()
use_logging = tk.BooleanVar(value=True)
blender_path = tk.StringVar()
selected_blender_version = tk.StringVar(value="Blender 3.6")

# Configure logging
log_file = "blender_render_log.txt"
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Function to start rendering
def start_render():
    global blender_process, crash_count
    render_folder_value = render_folder.get()
    blend_file_value = blend_file.get()
    start_frame_value = start_frame.get()
    end_frame_value = end_frame.get()
    use_logging_value = use_logging.get()
    blender_path_value = blender_path.get()

    # Check for already rendered frames and skip them
    existing_frames = [int(os.path.splitext(os.path.basename(png))[0]) for png in glob.glob(os.path.join(render_folder_value, '*.png'))]
    for frame in existing_frames:
        if frame >= start_frame_value and frame <= end_frame_value:
            start_frame_value = frame + 1

    # Start the initial Blender render
    blender_command = [blender_path_value, "-b", blend_file_value, "-s", str(start_frame_value), "-e", str(end_frame_value), "-a"]
    blender_process = subprocess.Popen(blender_command)
    crash_count = 0
    if use_logging_value:
        logging.info("Render started.")

# Function to stop rendering
def stop_render():
    global blender_process
    if blender_process.poll() is None:
        blender_process.kill()
        if use_logging.get():
            logging.warning("Render stopped.")

# Create the GUI elements
render_folder_label = tk.Label(root, text="Render Folder:")
render_folder_entry = tk.Entry(root, textvariable=render_folder)
render_folder_button = tk.Button(root, text="Browse", command=lambda: render_folder.set(filedialog.askdirectory()))

blend_file_label = tk.Label(root, text="Blend File:")
blend_file_entry = tk.Entry(root, textvariable=blend_file)
blend_file_button = tk.Button(root, text="Browse", command=lambda: blend_file.set(filedialog.askopenfilename(filetypes=[("Blend Files", "*.blend")])))
start_frame_label = tk.Label(root, text="Start Frame:")
start_frame_entry = tk.Entry(root, textvariable=start_frame)
end_frame_label = tk.Label(root, text="End Frame:")
end_frame_entry = tk.Entry(root, textvariable=end_frame)

use_logging_checkbox = tk.Checkbutton(root, text="Enable Logging", variable=use_logging)
blender_path_label = tk.Label(root, text="Blender Executable Path:")
blender_path_entry = tk.Entry(root, textvariable=blender_path)

blender_version_label = tk.Label(root, text="Select Blender Version:")
blender_version_menu = tk.OptionMenu(root, selected_blender_version, "Blender 3.6", "Blender 4.0", "Blender 5.0", "Blender 6.0")

start_button = tk.Button(root, text="Start Render", command=start_render)
stop_button = tk.Button(root, text="Stop Render", command=stop_render)

# Place GUI elements on the window
render_folder_label.pack()
render_folder_entry.pack()
render_folder_button.pack()

blend_file_label.pack()
blend_file_entry.pack()
blend_file_button.pack()

start_frame_label.pack()
start_frame_entry.pack()
end_frame_label.pack()
end_frame_entry.pack()

use_logging_checkbox.pack()
blender_path_label.pack()
blender_path_entry.pack()

blender_version_label.pack()
blender_version_menu.pack()

start_button.pack()
stop_button.pack()

# Run the GUI
root.mainloop()
