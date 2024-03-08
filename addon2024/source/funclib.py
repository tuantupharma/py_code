import bpy
from bpy import context
import os
import datetime

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
    

def set_output_render_path(filepath):
    getpath, nameblend  = get_file_and_project_path(filepath)
    new_path = getpath + "render\\"  + nameblend + "\\"

    bpy.context.scene.render.filepath = new_path




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

def get_current_time():
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    date = now.day
    month = now.month
    return hour, minute, date, month

# Example usage
    
#filepath = r"D:\job\makeaddon\lighting\testing.blend"
#get_file_and_project_path(filepath)