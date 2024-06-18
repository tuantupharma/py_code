import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import pandas as pd
import numpy as np


class VideoConverter:
    def init(self):
        self.root = tk.Tk()
        self.root.title("Video Converter")

      # GUI layout setup
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)

        self.input_label = tk.Label(self.frame, text="Input Image Sequence:")
        self.input_label.grid(row=0, column=0, padx=5, pady=5)
    
        self.input_path_entry = tk.Entry(self.frame, width=50)
        self.input_path_entry.grid(row=1, column=0, padx=5, pady=5)

        self.preset_label = tk.Label(self.frame, text="Select Presets from CSV:")
        self.preset_label.grid(row=2, column=0, padx=5, pady=5)
    
        self.preset_file_path = tk.StringVar()
        self.preset_button = tk.Button(self.frame, text="Select Presets", command=self.load_presets)
        self.preset_button.grid(row=3, column=0, padx=(5, 10))
    
        self.output_label = tk.Label(self.frame, text="Output File:")
        self.output_label.grid(row=4, column=0, padx=5, pady=5)
    
        self.output_path_entry.grid(tkshift=2, pady=5)

def load_presets(self):
    file_paths = [filedialog.askopenfilename()]
    preset_data = []
    for path in file_paths:
        df = pd.read_csv(path)
        preset_data.append(df.to_dict("records"))

    self.presets = preset_data[0] if len(preset_data) == 1 else None
    messagebox.showinfo("Preset Loaded", "Presets loaded successfully!")
    
def convert(self):
    input_path = self.input_path_entry.get()
    presets = self.presets if self.presets else None

    # Determine output size (1920x1080 or 1080x1920) based on input image's aspect ratio
    img = Image.open(input_path)
    width, height = img.size
    if abs(width - height) <= 5: # To account for rounding errors
        output_size = (1920, 1080)
    else:
        output_size = (1080, 1920)
    
    output_path = filedialog.asksaveasfilename(defaultextension=".mp4",
                                               filetypes=[("MP4 Files", "*.mp4")])

    # Call FFmpeg to convert the image sequence into an mp4 video with h264 codec
    command = f"ffmpeg -framerate 15 -i {input_path} -vcodec libx264 -s {output_size[0]}x{output_size[1]} -pix_fmt yuv420p {output_path}"
    subprocess.call(command, shell=True)

if name == "main":
    app = VideoConverter()
    app.root.mainloop()
