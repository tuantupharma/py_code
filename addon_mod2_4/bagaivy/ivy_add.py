import bpy
import os
from bpy.types import Operator
from bpy import context
import ntpath
import addon_utils
import time
import json
from pathlib import Path
import math
from . ivy_ui import IVY_OP_switchinput


class IVY_OP_add(Operator):
    """ Add ivy """
    bl_idname = "bagaivy.add_ivy"
    bl_label = 'Add Ivy'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        o = context.object
        ivy_pref = context.preferences.addons['BagaIvy'].preferences

        if ivy_pref.panel_asset_source == False:
            area = find_areas('ASSETS')
            if o is not None and o.type == 'MESH'and area is not None:
                win = find_window('ASSETS')
                if area.ui_type == 'ASSETS':
                    with context.temp_override(window=win, area = area):
                        return context.selected_assets
        else:
            if len(bpy.context.selected_objects) > 1 and o.type == 'MESH':
                        return context.selected_objects

    def execute(self, context):
        targets = bpy.context.selected_objects
        ivy_pref = context.preferences.addons['BagaIvy'].preferences

        if ivy_pref.panel_asset_source == False:            
            if find_areas('ASSETS').spaces.active.params.asset_library_reference == "ALL":
                Warning(message = "You must select the asset library you want to use in the Assets Browser", title = "'All' library not supported", icon = 'INFO')
                return {"FINISHED"}

    ###################################################################################
    # SELECT TARGETS
    ###################################################################################        
        if bpy.data.collections.get("Baga Ivy Generator") is not None:
            main_coll = bpy.data.collections["Baga Ivy Generator"]
            ivy_coll = bpy.data.collections.new("BIG_Ivy Generated") # IVY COLL
            main_coll.children.link(ivy_coll)

            target_coll = bpy.data.collections.new("BIG_Targets") # Targets
            ivy_coll.children.link(target_coll)

            ivy_asset_coll = bpy.data.collections.new("BIG_Ivy_Assets") # Ivy_Assets
            ivy_coll.children.link(ivy_asset_coll)
            ivy_asset_coll_name = ivy_asset_coll.name

            ivy_flowers_coll = bpy.data.collections.new("BIG_Ivy_Flowers") # Ivy_Assets
            ivy_coll.children.link(ivy_flowers_coll)
            ivy_flowers_coll_name = ivy_flowers_coll.name

            ivy_start_point_coll = bpy.data.collections.new("BIG_Ivy_Start_Point") # Ivy_Start_Point
            ivy_coll.children.link(ivy_start_point_coll)
            ivy_start_point_coll_name = ivy_start_point_coll.name

            ivy_start_effector = bpy.data.collections.new("BIG_Effector") # Ivy_Start_Point
            ivy_coll.children.link(ivy_start_effector)
            ivy_start_effector_name = ivy_start_effector.name

            ivy_sub_coll = bpy.data.collections.new("BIG_Ivy") # Ivy
            ivy_coll.children.link(ivy_sub_coll)
            ivy_sub_coll_name = ivy_sub_coll.name

            coll_targets = Collection_Add(self,context,ivy_coll.name,target_coll.name)
        else:
            coll_targets = Collection_Add(self,context,"BIG_Ivy Generated","BIG_Targets")
            ivy_asset_coll_name = "BIG_Ivy_Assets"
            ivy_flowers_coll_name = "BIG_Ivy_Flowers"
            ivy_start_point_coll_name = "BIG_Ivy_Start_Point"
            ivy_sub_coll_name = "BIG_Ivy"
            ivy_start_effector_name = "BIG_Effector"

        # IF EN MODE SOURCE 'VIEW 3D' only one target is possible
        for o in targets:
            if coll_targets[1] not in o.users_collection:
                coll_targets[1].objects.link(o)
        if context.object.name not in coll_targets[1].objects:
            coll_targets[1].objects.link(context.object)
        ivy_coll_name = coll_targets[0].name


    ###################################################################################
    # ASSETS IMPORT
    ###################################################################################
        coll_effector = Collection_Add(self,context,ivy_coll_name,ivy_start_effector_name)     


    ###################################################################################
    # ASSETS IMPORT
    ###################################################################################
        # FROM ASSET BROWSER
        if ivy_pref.panel_asset_source == False:
            area = find_areas('ASSETS')
            win = find_window('ASSETS')
            current_library_name = area.spaces.active.params.asset_library_reference

            if current_library_name == "LOCAL":
                library_path = Path(bpy.data.filepath)
            else:
                library_path = Path(context.preferences.filepaths.asset_libraries.get(current_library_name).path)
            coll_asset = Collection_Add(self,context,ivy_coll_name,ivy_asset_coll_name)
            coll_flower = Collection_Add(self,context,ivy_coll_name,ivy_flowers_coll_name)        
            
            is_flower = False
            with context.temp_override(window=win, area = area):
                print("Imported Assets :")
                assets_imported = []
                for asset_file in context.selected_assets :
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
                            coll_flower[1].objects.link(bpy.data.objects[asset_name])
                        else:
                            coll_asset[1].objects.link(bpy.data.objects[asset_name])
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
                                    coll_flower[1].objects.link(a)
                                else:
                                    coll_asset[1].objects.link(a)
                                
                            if inner_path == 'Collection':
                                bpy.data.collections.remove(bpy.data.collections[asset_name])
                        else:
                            print('"'+asset_name+'"' + " isn't a Collection or Object")


        # FROM 3D View
        else:
            coll_asset = Collection_Add(self,context,ivy_coll_name,ivy_asset_coll_name)
            coll_flower = Collection_Add(self,context,ivy_coll_name,ivy_flowers_coll_name)        

            target = bpy.context.active_object
            if target in targets:
                targets.remove(target)

            for asset in targets:
                is_flower = False
                asset.select_set(True)
                if 'flower' in asset.name:
                    is_flower = True
                    coll_flower[1].objects.link(asset)
                else:
                    coll_asset[1].objects.link(asset)



    ###################################################################################
    # SET START POINT
    ###################################################################################
        bpy.ops.mesh.primitive_ico_sphere_add(radius = 0.1, location=bpy.context.scene.cursor.location)
        start_point = bpy.context.selected_objects
        sp_coll = start_point[0].users_collection
        coll_start_point = Collection_Add(self,context,ivy_coll_name,ivy_start_point_coll_name)
        for s in start_point:
            coll_start_point[1].objects.link(s)
            s.hide_render = True
            s.display_type = 'WIRE'
            s.visible_shadow = False
            s.visible_volume_scatter = False
            s.visible_transmission = False
            s.visible_glossy = False
            s.visible_diffuse = False
            s.visible_camera = False
            s.name = "BIG_Start_Point"
            s.data.name = "BIG_Start_Point"
        
        for coll in sp_coll:            
            coll.objects.unlink(start_point[0]) 



    ###################################################################################
    # ADD IVY CURVE
    ###################################################################################    
        curve = bpy.data.curves.new('BagaIvy', 'CURVE')
        ivy_curve = bpy.data.objects.new(curve.name, curve)
        ivy_curve.data.resolution_u = 64
        ivy_curve.data.dimensions = '3D'
        ivy_curve.location = bpy.context.scene.cursor.location
        ivy_curve["BIG_Ivy"] = 1

        coll_ivy = Collection_Add(self,context,ivy_coll_name,ivy_sub_coll_name)
        coll_ivy[1].objects.link(ivy_curve)


    ###################################################################################
    # ADD MODIFIER
    ###################################################################################           
        new = ivy_curve.modifiers.new
        modifier = new(name="Baga_Ivy_Generator_V2", type='NODES')


    ###################################################################################
    # IMPORT AND SETUP IVY NODES
    ###################################################################################
        Add_NodeGroup(self,context,modifier)

        # SETUP COLLECTIONS
        modifier["Input_2"] = coll_targets[1]
        modifier["Input_3"] = coll_start_point[1]
        modifier["Input_24"] = coll_asset[1]
        modifier["Input_56"] = coll_effector[1]

        if is_flower == True:
            switch_bool_input('Input_36', modifier)
            # modifier["Input_36"] = 1
        modifier["Input_21"] = coll_flower[1]


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
                        # preset[0] = NOM_DU_PRESET
                        # preset[1] = LISTE DES INPUTS (NAME, Input_XX, Value) chaques
                        # preset[1][input] = [NAME, Input_XX, Value]
                        # preset[1][input][0] = "nom"
                        # preset[1][input][1] = 'Input_XX'
                        # preset[1][input][2] = Value
                        # exception for the vector type inputs : (NAME, Input_XX, ValueX, ValueY, ValueZ)

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

                                    update_disp_format = modifier.node_group.inputs[preset[1][input][0]]
                                    update_disp_format.default_value = update_disp_format.default_value
                                except:
                                    print(f"Input {input} not found, skipping to next one.")
                                    continue
                            break

        # IVY METHOD
        modifier["Input_81"] = ivy_pref.fast
        modifier["Input_82"] = ivy_pref.accurate
        modifier["Input_83"] = ivy_pref.precision

        
    ###################################################################################
    # UVs
    ###################################################################################
        if modifier["Input_81"]: #fast
            node_group = modifier.node_group
            node_from = node_group.nodes.get('bagaivy_generator_fast_uvs')
            node_to = node_group.nodes.get('bagaivy_generator_uvs')
            if node_from is not None and node_to is not None:
                socket_out = node_from.outputs[0]
                socket_in = node_to.inputs[0]
                node_group.links.new(socket_out, socket_in)
        elif modifier["Input_82"]: #accurate
            node_group = modifier.node_group
            node_from = node_group.nodes.get('bagaivy_generator_accurate_uvs')
            node_to = node_group.nodes.get('bagaivy_generator_uvs')
            if node_from is not None and node_to is not None:
                socket_out = node_from.outputs[0]
                socket_in = node_to.inputs[0]
                node_group.links.new(socket_out, socket_in)
        elif modifier["Input_83"]: #precision
            node_group = modifier.node_group
            node_from = node_group.nodes.get('bagaivy_generator_precision_uvs')
            node_to = node_group.nodes.get('bagaivy_generator_uvs')
            if node_from is not None and node_to is not None:
                socket_out = node_from.outputs[0]
                socket_in = node_to.inputs[0]
                node_group.links.new(socket_out, socket_in)


    ###################################################################################
    # MATERIAL
    ###################################################################################
        material = bpy.data.materials.get('BIG_Ivy_Bark')
        if material is not None:
            ivy_curve.data.materials.append(material)


    ###################################################################################
    # SWITCH AND START DRAW
    ###################################################################################
        bpy.context.view_layer.objects.active = ivy_curve
        bpy.ops.object.editmode_toggle()
        bpy.context.scene.tool_settings.curve_paint_settings.depth_mode = 'SURFACE'
        bpy.ops.wm.tool_set_by_id(name="builtin.draw")

        return {"FINISHED"}



def switch_bool_input(index, modifier):
    blender_version = bpy.app.version
    minimum_version = (3, 5, 0)
    if blender_version >= minimum_version:
        if modifier[index] == True:
            modifier[index] = False
        else:
            modifier[index] = True
    else:
        if modifier[index] == 1:
            modifier[index] = 0
        else:
            modifier[index] = 1
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.editmode_toggle()

    return None

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

###################################################################################
# ADD NODEGROUP TO THE MODIFIER
###################################################################################
def Add_NodeGroup(self,context,modifier):
    try:
        modifier.node_group = bpy.data.node_groups["Baga_Ivy_Generator_V2"]
    except:
        Import_Nodes(self,context)
        modifier.node_group = bpy.data.node_groups["Baga_Ivy_Generator_V2"]

###################################################################################
# IMPORT NODE GROUP
###################################################################################
def Import_Nodes(self,context):

    for mod in addon_utils.modules():
        if mod.bl_info['name'] == "Baga Ivy Generator":
            filepath = mod.__file__
            file_path = filepath.replace("__init__.py","Ivy_Node_Tree.blend")
        else: pass
    inner_path = "NodeTree"
    nodes_name = "Baga_Ivy_Generator_V2"

    bpy.ops.wm.append(
        filepath = os.path.join(file_path, inner_path, nodes_name),
        directory = os.path.join(file_path, inner_path),
        filename=nodes_name
        )

###################################################################################
# MANAGE COLLECTION
###################################################################################
def Collection_Add(self,context,ivy_coll_name,sub_coll_name):

    # Create collection and check if the main "Baga Collection" does not already exist
    if bpy.data.collections.get("Baga Ivy Generator") is None:
        main_coll = bpy.data.collections.new("Baga Ivy Generator") # MAIN
        bpy.context.scene.collection.children.link(main_coll)
        if bpy.data.collections.get(ivy_coll_name) is None:
            ivy_coll = bpy.data.collections.new(ivy_coll_name) # IVY COLL
            main_coll.children.link(ivy_coll)
        else:
            ivy_coll = bpy.data.collections.get(ivy_coll_name)
        sub_coll = bpy.data.collections.new(sub_coll_name) # SUB CATEGORY COLL
        ivy_coll.children.link(sub_coll)

    # If the main collection Bagapie already exist
    elif bpy.data.collections.get(sub_coll_name) is None:
        main_coll = bpy.data.collections["Baga Ivy Generator"]
        if bpy.data.collections.get(ivy_coll_name) is None:
            ivy_coll = bpy.data.collections.new(ivy_coll_name) # IVY COLL
            main_coll.children.link(ivy_coll)
        else:
            ivy_coll = bpy.data.collections.get(ivy_coll_name)
        sub_coll = bpy.data.collections.new(sub_coll_name) # SUB CATEGORY COLL
        ivy_coll.children.link(sub_coll)

    # If the main collection Bagapie_Scatter already exist
    else:
        ivy_coll = bpy.data.collections.get(ivy_coll_name)
        sub_coll = bpy.data.collections.get(sub_coll_name)

    return ivy_coll, sub_coll

###################################################################################
# DISPLAY WARNING
###################################################################################

def Warning(message = "", title = "Message Box", icon = 'INFO'):

    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)
