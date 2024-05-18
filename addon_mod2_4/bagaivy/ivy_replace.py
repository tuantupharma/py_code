import bpy
import os
from bpy.types import Operator
from bpy import context
import ntpath
import addon_utils
import time
import json
from pathlib import Path
from .ivy_add import Add_NodeGroup
import time
import math
        
class IVY_REPLACE_Ivy(bpy.types.Operator):
    """Replace the current ivy preset by the selected one in the Asset Browser"""
    bl_idname = "ivy.replace_preset"
    bl_label = "Delete Ivy"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        o = context.object
        area = find_areas('ASSETS')
        if o is not None and o.type == 'CURVE' and area is not None and o.modifiers["Baga_Ivy_Generator_V2"] is not None:
            win = find_window('ASSETS')
            if area.ui_type == 'ASSETS':
                with context.temp_override(window=win, area = area):
                    return context.selected_assets

    def execute(self, context):
        target = bpy.context.active_object
        ivy_pref = context.preferences.addons['BagaIvy'].preferences

        if ivy_pref.panel_asset_source == False:            
            if find_areas('ASSETS').spaces.active.params.asset_library_reference == "ALL":
                Warning(message = "You must select the asset library you want to use in the Assets Browser", title = "'All' library not supported", icon = 'INFO')
                return {"FINISHED"}
            

    ###################################################################################
    # GET COLLECTION AND REMOVE ASSETS
    ################################################################################### 
        ivy_colls = target.users_collection
        for coll in ivy_colls:
            if coll.name.startswith('BIG_Ivy'):
                for parent_collection in bpy.data.collections:
                    if coll.name in parent_collection.children.keys():
                        if parent_collection.name.startswith('BIG_Ivy Generated'):
                            main_coll = parent_collection
                            ivy_coll = coll
                            for colls in parent_collection.children.keys():
                                if colls.startswith('BIG_Targets'):
                                    target_coll = bpy.data.collections[colls]
                                elif colls.startswith('BIG_Ivy_Assets'):
                                    assets_coll = bpy.data.collections[colls]
                                elif colls.startswith('BIG_Ivy_Start_Point'):
                                    start_point_coll = bpy.data.collections[colls]
                                elif colls.startswith('BIG_Effector'):
                                    start_effector = bpy.data.collections[colls]
                                elif colls.startswith('BIG_Ivy_Flowers'):
                                    flower_coll = bpy.data.collections[colls]

        # main_coll         Collection Principale : BIG_Ivy Generated           KEEP
        # ivy_colls[0]      Ivy coll list (BIG_Ivy)                             KEEP
        # target_coll       Objects target (BIG_Targets)                        KEEP
        # assets_coll       Leaves (BIG_Ivy_Assets)                             PURGE
        # flower_coll       Flowers (BIG_Ivy_Flowers)                           PURGE
        # objects_coll      Collection List (BIG_Ivy_Start_Point, BIG_Ivy)      KEEP
        # start_point_coll  Start Points (BIG_Ivy_Start_Point)                  KEEP
        # start_effector    Effectors (BIG_Effector)                            KEEP

        to_delete = []
        for ob in assets_coll.objects:
            to_delete.append(ob)
        for ob in flower_coll.objects:
            to_delete.append(ob)

        area = find_areas('ASSETS')
        win = find_window('ASSETS')
        current_library_name = area.spaces.active.params.asset_library_reference

        if current_library_name == "LOCAL":
            library_path = Path(bpy.data.filepath)
        else:
            library_path = Path(context.preferences.filepaths.asset_libraries.get(current_library_name).path)
        
        is_flower = False
        with context.temp_override(window=win, area = area):
            print("Imported Assets :")
            assets_imported = []

            for asset_file in context.selected_assets:
                asset_fullpath = library_path / asset_file.full_path
                if current_library_name == "LOCAL":
                    asset_fullpath /= asset_file.local_id.name

                asset_filepath = asset_fullpath.parent.parent
                inner_path = ntpath.basename(ntpath.dirname(asset_fullpath))
                asset_name = ntpath.basename(asset_fullpath)
                print('"'+asset_name+'"' + " from type : " + inner_path)

                time.sleep(1)
                try:
                    bpy.data.objects[asset_name].select_set(True)
                    if 'flower' in asset_name or 'fruit' in asset_name or 'Flower' in asset_name or 'Fruit' in asset_name:
                        is_flower = True
                        flower_coll.objects.link(bpy.data.objects[asset_name])
                    else:
                        assets_coll.objects.link(bpy.data.objects[asset_name])
                    assets_imported.append(asset_name)
                except:
                    if inner_path == 'Collection' or inner_path == 'Object':
                        bpy.ops.wm.append(
                            filepath=os.path.join(asset_filepath, inner_path, asset_name),
                            directory=os.path.join(asset_filepath, inner_path),
                            filename=asset_name
                            )
                        objs = bpy.context.selected_objects
                        assets_imported.append(asset_name)
                        for a in objs:
                            for col in a.users_collection:
                                col.objects.unlink(a)
                                
                            if 'flower' in a.name or 'fruit' in a.name or 'Flower' in a.name or 'Fruit' in a.name:
                                is_flower = True
                                flower_coll.objects.link(a)
                            else:
                                assets_coll.objects.link(a)
                            
                        if inner_path == 'Collection':
                            bpy.data.collections.remove(bpy.data.collections[asset_name])
                    else:
                        print('"'+asset_name+'"' + " isn't a Collection or Object")  


        # REMOVE ASSETS (LEAVES AND FLOWERS)
        for ob in to_delete:
            if ob.name in assets_coll.objects:
                assets_coll.objects.unlink(ob)
            elif ob.name in flower_coll.objects:
                flower_coll.objects.unlink(ob)
            bpy.data.objects.remove(ob, do_unlink=True)


        # IVY METHOD
        modifier = target.modifiers["Baga_Ivy_Generator_V2"]
        fast = modifier["Input_81"]
        accurate = modifier["Input_82"]
        precision = modifier["Input_83"]

    ###################################################################################
    # REMOVE MODIFIER
    ################################################################################### 
        for modifier in target.modifiers:
            if modifier.name == "Baga_Ivy_Generator_V2" or modifier.name == "Baga_Ivy_Generator":
                bpy.ops.object.modifier_remove(modifier=modifier.name)


    ###################################################################################
    # ADD MODIFIER
    ###################################################################################           
        new = target.modifiers.new
        modifier = new(name="Baga_Ivy_Generator_V2", type='NODES')


    ###################################################################################
    # IMPORT AND SETUP IVY NODES
    ###################################################################################
        Add_NodeGroup(self,context,modifier)

        # SETUP COLLECTIONS
        modifier["Input_2"] = target_coll
        modifier["Input_3"] = start_point_coll
        modifier["Input_24"] = assets_coll
        modifier["Input_56"] = start_effector

        if is_flower == True:
            modifier["Input_36"] = 1
        modifier["Input_21"] = flower_coll

        modifier["Input_10"] = "Generation Method"
        modifier["Input_9"] = "Ivy Growth"
        modifier["Input_14"] = "Leaves"
        modifier["Input_16"] = "Leaves Source"
        modifier["Input_64"] = "Animation"
        modifier["Input_86"] = "Ivy Modes - DO NOT CHANGE"

        # SETUP PRESETS
        if ivy_pref.panel_asset_source == False:
            if inner_path == 'Collection':

                for mod in addon_utils.modules():
                    if mod.bl_info['name'] == "Baga Ivy Generator":
                        filepath = mod.__file__
                        file_path = filepath.replace("__init__.py","")
                        presets_path = file_path + "/ivy_presets_param.json"

                with open(presets_path, 'r') as f:
                    data = json.load(f)
                    for idx, preset in enumerate(data):
                        # preset[0]                 NOM_DU_PRESET
                        # preset[1]                 LISTE DES INPUTS (NAME, Input_XX, Value) chaques
                        # preset[1][input]          [NAME, Input_XX, Value]
                        # preset[1][input][0]       "nom"
                        # preset[1][input][1]       'Input_XX'
                        # preset[1][input][2]       Value
                        # exception for vector type inputs : (NAME, Input_XX, ValueX, ValueY, ValueZ)

                        if preset[0] in assets_imported:
                            print("Preset Index = "+str(idx))
                            modifier["Input_120"] = preset[0]
                            for input in preset[1]:
                                try:
                                    if len(preset[1][input]) > 3:
                                        modifier[input][0] = preset[1][input][2]
                                        modifier[input][1] = preset[1][input][3]
                                        modifier[input][2] = preset[1][input][4]
                                    else:
                                        modifier[input] = preset[1][input][2]

                                    # KEEP IT !
                                    # It's a potato fix to update value display
                                    # IDK why it works
                                    # But it works
                                    update_disp_format = modifier.node_group.inputs[preset[1][input][0]]
                                    update_disp_format.default_value = update_disp_format.default_value
                                except:
                                    print(f"Input {input} not found, skipping to next one.")
                                    continue
                            break
        # IVY METHOD
        modifier["Input_81"] = fast
        modifier["Input_82"] = accurate
        modifier["Input_83"] = precision

        return {'FINISHED'}


###################################################################################
# FIND AREAS
###################################################################################
def find_areas(type):
    areas_list = []
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.ui_type == type:
                return area
    return None

###################################################################################
# FIND WINDOWS
###################################################################################
def find_window(type):
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.ui_type == type:
                return window
    return None