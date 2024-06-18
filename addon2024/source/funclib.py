import bpy
from bpy import context
import os
import datetime
import subprocess
def get_file_and_project_path(filepath):
    # Get the absolute path of the current .py file
    #current_file_path = os.path.abspath(__file__)
    
    # Get the project path by removing the current file name from the absolute path
    project_path = os.path.dirname(filepath)
    print("project Name: ", project_path)
    # Get the file name from the filepath
    file_name = os.path.basename(filepath)
    
    project_pathtr = ""

    folders = project_path.split(os.sep)  # Split the path into individual folder names
    print("File Name: ", folders)
    for i in range(len(folders)-1):
        if  "asset" not in folders[i] and  "Asset" not in folders[i]:
            project_pathtr = project_pathtr + folders[i] + "\\"
    
    
    # Print the file name and project path to the console
    file_name = file_name[:file_name.rfind('.')]
    print("File Name: ", file_name)
    print("Project Path: ", project_pathtr)
    return project_pathtr , file_name


def set_output_check(projectloc):
    getpath, nameblend  = get_file_and_project_path(projectloc)
    
    hour, minute, date, month = get_current_time()
    datetoday = str(hour) + "H" + str(minute) + "_" + str(date) + "T" + str(month)
    
    new_path = getpath + "check\\" + datetoday + "_" + nameblend + "_"

    bpy.context.scene.render.filepath = new_path
    print(new_path)

def open_check_folder():
    projectloc = bpy.data.filepath
    getpath, dumy = get_file_and_project_path(projectloc)
    new_path = getpath + "check\\"
    print(new_path)
    path = rf"{new_path}\\"
    if os.name == 'nt':  # Checking for Windows OS (OS name is 'nt')
        try:
            os.startfile(path)
        except Exception as e:
            print("An error occurred while trying to open the folder.")
            raise
    else:
        print("This script can only be run on Windows")
# Open Windows Explorer with the given path
    
    
    


def set_output_render_path(filepath):
    getpath, nameblend  = get_file_and_project_path(filepath)
    new_path = getpath + "render\\"  + nameblend + "\\"

    bpy.context.scene.render.filepath = new_path


#preset sectors

def set_render_png_output():
    # Set the render output format to PNG
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    
    # Set the color mode to RGBA
    bpy.context.scene.render.image_settings.color_mode = 'RGBA'
    
    # Set the bit depth to 8-bit
    bpy.context.scene.render.image_settings.color_depth = '8'
    
    # Set the compression to 90%
    bpy.context.scene.render.image_settings.compression = 90

    
def set_render_exr_output():
    # Set the render output format to PNG
    bpy.context.scene.render.image_settings.file_format = 'OPEN_EXR'
    
    # Set the color mode to RGBA
    bpy.context.scene.render.image_settings.color_mode = 'RGBA'
    
    # Set the bit depth to 8-bit
    bpy.context.scene.render.image_settings.color_depth = '16'
    
    bpy.context.scene.render.image_settings.exr_codec = 'DWAB'  
    
    
def set_output_render_as_mp4_h264():
    # Set the output file format to FFMPEG
    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
    
    # Set the container and codec for the output file
    bpy.context.scene.render.ffmpeg.format = 'MPEG4'
    bpy.context.scene.render.ffmpeg.codec = 'H264'    

def render_viewport_animation(context):
    # get the current active camera
    camera = context.scene.camera
    # get the original render engine
    original_engine = context.scene.render.engine
    # set the render engine to Workbenchn
    #context.scene.render.engine = 'BLENDER_WORKBENCH'
    # set the render resolution to match the viewport
    #context.scene.render.resolution_x = context.region.width
    #context.scene.render.resolution_y = context.region.height
    # set the render camera to the active camera
    context.scene.render.use_multiview = False
    
    #context.scene.render.views_format = 'SINGLE' # remove or comment out this line
    context.scene.render.image_settings.views_format = 'INDIVIDUAL'
    context.scene.render.use_compositing = False
    context.scene.render.use_sequencer = False
    # render the animation
    #bpy.ops.render.render(animation=True, write_still=True)
    for window in context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces.active.region_3d.view_perspective = 'CAMERA'
                #bpy.ops.view3d.view_camera()
                bpy.ops.render.opengl(animation=True)  
    # restore the original render engine
    context.scene.render.engine = original_engine

def viewportrender():
 old_path = bpy.context.scene.render.filepath
 print(bpy.context.scene.render.filepath)

 set_output_render_as_mp4_h264()
 print(bpy.data.filepath)
 set_output_check(bpy.data.filepath)
 render_viewport_animation(bpy.context)
 set_render_png_output()
 if old_path == "" or old_path == "\\tmp\\":
  set_output_render_path(bpy.data.filepath)
 else : bpy.context.scene.render.filepath = old_path
 open_check_folder()

def get_current_time():
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    date = now.day
    month = now.month
    return hour, minute, date, month


def create_video_cv():
    # Set the output video file path
    input_folder = bpy.context.scene.render.filepath
    image_pattern =''
    if input_folder.endswith('\\'):  # Checks whether the folder ends with a backslash.
            image_pattern =''
    else:
            image_pattern = os.path.basename(input_folder)
            input_folder = os.path.dirname(input_folder)
    fps = bpy.context.scene.render.fps 
    output_file = os.path.join(input_folder, "video.mp4")
    

    # Get the list of image files in the input folder
    image_files = sorted([f for f in os.listdir(input_folder) if f.startswith(image_pattern.split("#")[0])])

    # Read the first image to get its dimensions
    first_image_path = os.path.join(input_folder, image_files[0])
    first_image = cv2.imread(first_image_path)
    height, width, channels = first_image.shape

    # Create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Specify the video codec
    video_writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    # Iterate through the image files and write them to the video
    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        image = cv2.imread(image_path)
        video_writer.write(image)

    # Release the VideoWriter
    video_writer.release()

    print("Video creation completed!")



def combine_image_sequence_to_mp4():
    # Get the current scene
    scene = bpy.context.scene

    # Get frame rate and render output path from the current blend file
    frame_rate = scene.render.fps
    frame_rate_time=1/frame_rate
    render_output_path = bpy.path.abspath(scene.render.filepath)
    file_format = scene.render.image_settings.file_format.lower()

    # Extract the directory and prefix from the render output path
    render_dir, render_prefix = os.path.split(render_output_path)
    if not render_dir:
        render_dir = os.path.dirname(render_output_path)
        render_prefix = os.path.basename(render_output_path)
    
    # Ensure the render output directory exists
    if not os.path.exists(render_dir):
        print(f"Render directory {render_dir} does not exist.")
        return

    # Collect all files matching the prefix and format
    image_files = sorted([f for f in os.listdir(render_dir) if f.startswith(render_prefix) and f.lower().endswith(file_format)])

    # Ensure there are images to process
    if not image_files:
        print("No rendered images found.")
        return

    # Create a text file with the list of images
    file_list_path = os.path.join(render_dir, "image_list.txt")
    with open(file_list_path, 'w') as file_list:
        for image_file in image_files:
            file_list.write(f"file '{os.path.join(render_dir, image_file)}'\nduration {frame_rate_time}\n")
    # create prefix  
    projectloc = bpy.data.filepath
    getpath, blend_file_name = get_file_and_project_path(projectloc)     
    hour, minute, date, month = get_current_time()
    date_today = str(hour) + "H" + str(minute) + "_" + str(date) + "T" + str(month)
    # Create the output MP4 file path
    mp4name = str(blend_file_name)+"_"+ str(date_today) + ".mp4"
    print(f"MP4 name created: {mp4name}")
    output_mp4_path = os.path.join(render_dir, mp4name)
    print(mp4name)

    # Combine the images into an MP4 using ffmpeg with improved quality settings
   
    ffmpeg_command = (
        f"ffmpeg -r {frame_rate} -f concat -safe 0 -i {file_list_path}  -c:v h264_nvenc -preset slow -b:v 30M -pix_fmt yuv420p -y -minrate 10M {output_mp4_path}"
    )
    os.system(ffmpeg_command)
    
    print(f"MP4 file created: {output_mp4_path}")
# Example usage
    
#filepath = r"D:\job\makeaddon\lighting\testing.blend"
#get_file_and_project_path(filepath)