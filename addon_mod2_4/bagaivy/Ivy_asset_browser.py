import bpy
import addon_utils
from bpy.types import Operator

class IVY_OP_SetupAssetBrowser(Operator):
    """Add BagaIvy's assets library in the asset browser"""
    bl_idname = "bagaivy.ivyassetslibrary"
    bl_label = "Install BagaIvy's assets as Asset Library"
    def execute(self, context):
        
        # GET THE ASSETS PATH
        for mod in addon_utils.modules():
                if mod.bl_info['name'] == "Baga Ivy Generator":
                    filepath = mod.__file__
                    file_path = filepath.replace("__init__.py","")

        prefs = bpy.context.preferences
        filepaths = prefs.filepaths
        asset_libraries = filepaths.asset_libraries

        add = True
        for lib in asset_libraries:
            if lib.name == "BagaIvy Generator":
                Warning(message = "Lbrary already installed.", title = "INFO", icon = 'INFO')
                add = False
        if add == True:
            bpy.ops.preferences.asset_library_add(directory = file_path)
            asset_libraries[len(asset_libraries)-1].name = "BagaIvy Generator"
            Warning(message = "Library installed ! It's now visible in the Asset Browser > BagaIvy.", title = "Done !", icon = 'INFO')
        
        return {'FINISHED'}


###################################################################################
# WARNING
###################################################################################

def Warning(message = "", title = "Message Box", icon = 'INFO'):

    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

