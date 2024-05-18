import bpy
import os
import bpy.utils.previews
import addon_utils

previews = bpy.utils.previews.new()

def import_icons():
  global previews

  for mod in addon_utils.modules():
        if mod.bl_info['name'] == "Baga Ivy Generator":
            filepath = mod.__file__
            icons_path = filepath.replace("__init__.py","tooltips" + os.sep)

  for icon in os.scandir(icons_path):
    previews.load(icon.name.split(".")[0], icon.path, "IMAGE")

def unload_icons():
  global previews
  bpy.utils.previews.remove(previews)