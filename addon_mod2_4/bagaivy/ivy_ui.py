import bpy
import os
import bpy.utils.previews
import ntpath
import addon_utils
import time
from bpy.types import Menu, Panel, UIList, Operator
from . import icons
from pathlib import Path

def check_library_exists(library_name):
    prefs = bpy.context.preferences
    asset_libraries = prefs.filepaths.asset_libraries

    for lib in asset_libraries:
        if lib.name == library_name:
            return True
    return False

class IVY_PT_Panel(bpy.types.Panel):
    """BagaIvy Generator"""
    bl_idname = "IVY_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "BagaIvy"
    bl_label = "Baga Ivy Generator"

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        # ALPHA  & Beta
        # col_alert = col.column()
        # col_alert.alert = True
        # col_alert.label(text="BETA VERSION")
        # col_alert.label(text="ONLY FOR TESTING")

        obj = context.object

        # GET ADDON PREF
        ivy_pref = context.preferences.addons['BagaIvy'].preferences

        if not check_library_exists("BagaIvy Generator"):
            button=col.column()
            button.scale_y=3
            button.operator("bagaivy.ivyassetslibrary", text="Setup BagaIvy Asset Library")
            return

        ###################################################################################
        # IF IVY IS SELECTED
        ###################################################################################  
        if obj and "BIG_Ivy" in obj and "_Bake" not in obj.name:
                try:
                    ivy_modifier = obj.modifiers["Baga_Ivy_Generator_V2"]
                    is_v2 = True
                except KeyError:
                    ivy_modifier = obj.modifiers["Baga_Ivy_Generator"]
                    is_v2 = False


                col = layout.column(align=False)

                if "Input_82" in ivy_modifier:

                    main = col.row(align=True)
                    main.operator("bagaivy.switch_1", depress = ivy_modifier["Input_81"], text = "Fast")
                    main.operator("bagaivy.switch_2", depress = ivy_modifier["Input_82"], text = "Accurate")
                    main.operator("bagaivy.switch_3", depress = ivy_modifier["Input_83"], text = "Precision")

                
                ###################################################################################
                # ACCURATE
                ###################################################################################  
                if ivy_modifier.get("Input_82", True):

                    # IVY ABOUT MODE
                    if "Input_82" in ivy_modifier:
                        if ivy_pref.panel_sub_about == False:
                            col.prop(ivy_pref, 'panel_sub_about', text = "About Accurate mode", emboss = True, icon = "TRIA_RIGHT")
                        else:
                            box = col.box()
                            box.prop(ivy_pref, 'panel_sub_about', text = "About Accurate mode :", emboss = False, icon = "TRIA_DOWN")
                            col_about = box.column(align=True)
                            col_about.scale_y=0.8
                            text = "Generates realistic ivy, including branch ramifications."
                            lines = split_text(text, 28)
                            for line in lines: col_about.label(text=line)
                            col_about.separator(factor = 1)
                            text = "This generator requires one or more 'Start Points' to determine the growth onset. By default, it uses the 3D Cursor's position for the first 'Start Point', but you can add as many as you wish. See 'Ivy Growth'."
                            lines = split_text(text, 28)
                            for line in lines: col_about.label(text=line)
                            col_about.separator(factor = 1)
                            text = "We recommend using this ivy for elements ranging from background to foreground."
                            lines = split_text(text, 28)
                            for line in lines: col_about.label(text=line)

                    if bpy.context.object.mode == 'OBJECT' and "Input_82" in ivy_modifier:
                        cobox = col.box().column(align=True)
                        if ivy_modifier["Input_120"] != "":
                            cobox.label(text = ' '.join(word.capitalize() for word in ivy_modifier["Input_120"].split('_')))
                        row = cobox.row(align=True)
                        row.scale_y = 2
                        row.operator("ivy.replace_preset", text = "Replace Presets")
                        tips = row.operator("bagaivy.tooltips", text="", emboss = True, depress = False, icon = 'INFO')
                        tips.message = 'You can select another preset in the asset browser to replace the current ivy. Any changes you may have made to this ivy will not be saved.'
                        tips.title = "Replace Presets"
                        tips.image = "None"
                        tips.scale = 10
                        tips.url = "None"
                    col.separator(factor = 1.5)

                    # IVY GROWTH
                    if ivy_pref.panel_sub_distribution == False:
                        col.separator(factor = 0.5)
                        col.prop(ivy_pref, 'panel_sub_distribution', text = "Ivy Growth", emboss = False)
                        col.separator(factor = 1.5)
                    else:
                        box = col.box()
                        box.prop(ivy_pref, 'panel_sub_distribution', text = "Ivy Growth", emboss = False)

                        subcoll = box.column(align=True)
                        subcoll.prop(ivy_modifier, '["Input_53"]', text="Trunk Max Length")
                        subcoll.prop(ivy_modifier, '["Input_13"]', text="Branch Max Length")
                        subcoll.prop(ivy_modifier, '["Input_32"]', text=" Ivy Propagation")
                        subcoll.separator(factor = 0.4)
                        subcoll.prop(ivy_modifier, '["Input_8"]', text="Branch Density")

                        row = box.row()
                        row.label(text="Ivy Resolution :")
                        tips = row.operator("bagaivy.tooltips", text="", emboss = False, depress = False, icon = 'INFO')
                        tips.message = 'Overall resolution of the ivy. In case the generation becomes too long, reduce the resolution in the viewport to greatly improve performance.'
                        tips.title = "Resolution"
                        tips.image = "None"
                        tips.scale = 10
                        tips.url = "None"
                        row = box.row(align = True)
                        row.prop(ivy_modifier, '["Input_29"]', text="Viewport")
                        row.prop(ivy_modifier, '["Input_33"]', text="Render")

                        
                        if bpy.context.object.mode == 'OBJECT':

                            subcoll = box.column(align=True)
                            row = subcoll.row(align=True)
                            row.label(text="Target")
                            tips = row.operator("bagaivy.tooltips", text="", emboss = False, depress = False, icon = 'INFO')
                            tips.message = 'Ivy needs to know what surface it can grow on. Easily add or remove objects to grow on.'
                            tips.title = "Ivy target"
                            tips.image = "None"
                            tips.scale = 10
                            tips.url = "https://youtu.be/dh9fl1J59yo"
                            row = subcoll.row(align=True)
                            row.scale_y = 1.8
                            add = row.operator("ivyadd.target", text= "Add", icon = 'ADD')
                            add.index = 2
                            remove = row.operator("ivyremove.target", text= "Remove", icon = 'REMOVE')
                            remove.index = 2


                            #ADD START POINT
                            subcoll.separator(factor = 0.4)
                            row = subcoll.row(align= True)
                            row.operator("ivyadd.startpoint", text= "Add Start Point to 3D Cursor", icon = 'ADD')
                            tips = row.operator("bagaivy.tooltips", text="", depress = False, icon = 'INFO')
                            tips.message = 'Ivy needs to know where it starts to grow. These points are defined by "start points" (meshes) which by their proximity to the path (curves) will give the ivy a starting point to grow. You can add as many as you like.'
                            tips.title = "Start Point"
                            tips.image = "None"
                            tips.scale = 10
                            tips.url = "https://youtu.be/riZNnMEZDNE"

                        elif bpy.context.object.mode == 'EDIT':
                            row = box.row()
                            row.scale_y = 3
                            row.operator("ivy.draw", text= "EXIT", icon = 'LOOP_BACK')

                        
                        box = box.box()
                        box.prop(ivy_pref, 'panel_sub_distribution_avanced', text = "Advanced ", emboss = True)
                        if ivy_pref.panel_sub_distribution_avanced == True:

                            subcoll = box.column(align=True)
                            subcoll.prop(ivy_modifier, '["Input_80"]', text="Surface Offset")
                            row = subcoll.row(align= True)
                            row.label(text="Precision")
                            tips = row.operator("bagaivy.tooltips", text="", depress = False, icon = 'INFO', emboss = False)
                            tips.message = 'Increases or decreases the precision of the branches in relation to the trunk. A high value will tend to round off the growth contour of the ivy. This is directly related to "Network Density".'
                            tips.title = "Ivy's Precision"
                            tips.image = "None"
                            tips.scale = 10
                            subcoll.prop(ivy_modifier, '["Input_28"]', text="Trunk")
                            subcoll.prop(ivy_modifier, '["Input_27"]', text="Branch")

                            subcoll = box.column(align=True)
                            row = subcoll.row(align= True)
                            row.label(text="Network Density")
                            tips = row.operator("bagaivy.tooltips", text="", depress = False, icon = 'INFO', emboss = False)
                            tips.message = 'The branches are created through an invisible mesh, this value allows you to change the resolution of this mesh. Increase to reduce its resolution, decrease to increase the resolution of the mesh.'
                            tips.title = "Ivy's Network"
                            tips.image = "None"
                            tips.scale = 10
                            subcoll.prop(ivy_modifier, '["Input_30"]', text="Trunk")
                            subcoll.prop(ivy_modifier, '["Input_31"]', text="Branch")
                        col.separator(factor = 2.5)


                    # LEAVES
                    if ivy_pref.panel_sub_leaf == False:
                        col.separator(factor = 0.5)
                        col.prop(ivy_pref, 'panel_sub_leaf', text = "Leaves", emboss = False)
                        col.separator(factor = 1.5)
                    else:
                        box = col.box()
                        box.prop(ivy_pref, 'panel_sub_leaf', text = "Leaves", emboss = False)
                        col_new = box.column(align=True)
                        col_new.prop(ivy_modifier, '["Input_15"]', text="Leaves Density")
                        col_new.prop(ivy_modifier, '["Input_61"]', text="Distance Min")

                        if "Input_82" in ivy_modifier:
                            subcoll = box.column(align=True)
                            subcoll.label(text = "Leaves Scale :")
                            row = subcoll.row(align = True)
                            row.prop(ivy_modifier, '["Input_196"]', text="End")
                            row.prop(ivy_modifier, '["Input_197"]', text="Start")

                        subcoll = box.column(align=True)
                        subcoll.label(text = "Leaves Random Scale :")
                        row = subcoll.row(align = True)
                        row.prop(ivy_modifier, '["Input_17"]', text="Min")
                        row.prop(ivy_modifier, '["Input_18"]', text="Max")
                        
                        col_two=box.column(align=True)
                        row = col_two.row(align=True)
                        row.scale_y = 1.8
                        add = row.operator("ivyadd.asset", text= "Add Leaf", icon = 'ADD')
                        add.index = 24

                        row = col_two.row(align=True)
                        row.scale_y = 0.9
                        row.label(text="Source :")
                        row.prop(ivy_pref, 'panel_asset_source', text = "View 3D",  toggle = True)
                        row.prop(ivy_pref, 'panel_asset_source', text = "Asset Browser",  toggle = True, invert_checkbox=True)

                        col_two.separator(factor = 0.6)
                        row = col_two.row(align=True)
                        row.scale_y = 1.8
                        remove = row.operator("ivyremove.asset", text= "Remove Leaf", icon = 'REMOVE')
                        remove.index = 24

                        box = box.box()
                        box.prop(ivy_pref, 'panel_sub_leaf_avanced', text = "Advanced ", emboss = True)
                        if ivy_pref.panel_sub_leaf_avanced == True:
                            box.prop(ivy_modifier, '["Input_44"]', text="Alternating rotation")
                            box.prop(ivy_modifier, '["Input_45"]', text="Random Rotation")

                            box.label(text = "Inclination :")
                            row = box.row(align = True)
                            row.prop(ivy_modifier, '["Input_46"]', text="Min")
                            row.prop(ivy_modifier, '["Input_47"]', text="Max")
                            box.prop(ivy_modifier, '["Input_79"]', text="Offset Leaves Local")
                            box.prop(ivy_modifier, '["Input_55"]', text="Rotation Local")
                            box.prop(ivy_modifier, '["Input_58"]', text="Align Z Global")
                            
                        if ivy_modifier["Input_26"] == True:
                            col_tree=box.column(align=True)
                            col_tree.alert = True
                            col_tree.label(text="Leaf are disabled :")
                            col_tree.operator('switch.buttonivy', depress = ivy_modifier["Input_26"], text = "Use Leaf", icon = 'ERROR').index = "Input_26"
                        col.separator(factor = 2.5)


                    # FLOWERS
                    if ivy_pref.panel_sub_flower == False:
                        col.separator(factor = 0.5)
                        col.prop(ivy_pref, 'panel_sub_flower', text = "Flowers/Fruits", emboss = False)
                        col.separator(factor = 1.5)
                    else:
                        box = col.box()
                        box.prop(ivy_pref, 'panel_sub_flower', text = "Flowers/Fruits", emboss = False)
                        col_new = box.column(align=True)
                        if "Input_82" in ivy_modifier:
                            box.prop(ivy_modifier, '["Input_168"]', text="Animation")
                        col_new.prop(ivy_modifier, '["Input_25"]', text="Flowers Probability")

                        box.label(text = "Flowers Random Scale :")
                        row = box.row(align = True)
                        row.prop(ivy_modifier, '["Input_41"]', text="Min")
                        row.prop(ivy_modifier, '["Input_42"]', text="Max")
                        
                        if "Input_82" in ivy_modifier:
                            box.label(text = "Random Rotation")
                            row = box.row(align = True)
                            row.prop(ivy_modifier, '["Input_195"]', text="")
                        
                        col_two=box.column(align=True)
                        row = col_two.row(align=True)
                        row.scale_y = 1.8
                        add = row.operator("ivyadd.asset", text= "Add Flower", icon = 'ADD')
                        add.index = 21

                        row = col_two.row(align=True)
                        row.scale_y = 0.9
                        row.label(text="Source :")
                        row.prop(ivy_pref, 'panel_asset_source', text = "View 3D",  toggle = True)
                        row.prop(ivy_pref, 'panel_asset_source', text = "Asset Browser",  toggle = True, invert_checkbox=True)

                        col_two.separator(factor = 0.6)
                        row = col_two.row(align=True)
                        row.scale_y = 1.8
                        remove = row.operator("ivyremove.asset", text= "Remove Flower", icon = 'REMOVE')
                        remove.index = 21

                        if ivy_modifier["Input_36"] == False:
                            col_tree=box.column(align=True)
                            col_tree.alert = True
                            col_tree.label(text="Flowers are disabled :")
                            col_tree.operator('switch.buttonivy', depress = ivy_modifier["Input_36"], text = "Use Flower", icon = 'ERROR').index = "Input_36"
                                
                        box = box.box()
                        row = box.row(align=True)
                        row.prop(ivy_pref, 'panel_sub_flower_avanced', text = "Advanced ", emboss = True)
                        tips = row.operator("bagaivy.tooltips", text="", depress = False, icon = 'INFO', emboss = False)
                        tips.message = 'Parameters : Alternating Rotation, Random Rotation and Inclination are common between leaves and flowers. You can set them in the Leaves panel.'
                        tips.title = "Animation Method"
                        tips.image = "None"
                        tips.scale = 10
                        tips.url = "None"
                        if ivy_pref.panel_sub_flower_avanced == True:
                            box.prop(ivy_modifier, '["Input_78"]', text="Offset Flower Local")
                            box.prop(ivy_modifier, '["Input_54"]', text="Rotation Local")
                            box.prop(ivy_modifier, '["Input_57"]', text="Align Z Global")
                        col.separator(factor = 2.5)


                    # TRUNK
                    if ivy_pref.panel_sub_trunk == False:
                        col.separator(factor = 0.5)
                        col.prop(ivy_pref, 'panel_sub_trunk', text = "Trunk", emboss = False)
                        col.separator(factor = 1.5)
                    else:
                        box = col.box()
                        box.prop(ivy_pref, 'panel_sub_trunk', text = "Trunk", emboss = False)
                        
                        subcoll = box.column(align=True)
                        subcoll.prop(ivy_modifier, '["Input_11"]', text="Trunk Radius")
                        subcoll.prop(ivy_modifier, '["Input_12"]', text="Branch Radius")

                        box.label(text="Material :")
                        row = box.row(align=True)
                        row.prop_search(ivy_modifier, '["Input_48"]', bpy.data, "materials", text="", icon="MATERIAL")

                        tips = row.operator("bagaivy.tooltips", text="", depress = False, icon = 'INFO')
                        tips.message = 'You can set any shader here. If you use the default shader it will be displayed here. UVs are created by default, you can use them in your own shader by using the Attribute node with the attribute "UVs".'
                        tips.title = "Material"
                        tips.image = "None"
                        tips.scale = 10
                        tips.url = "None"

                        bark_mat = ivy_modifier['Input_48']
                        if bark_mat is not None:
                            if bark_mat.name.startswith('BIG_Ivy_Bark'):
                                bark_node_group = bark_mat.node_tree.nodes['BIG_Ivy_Bark_Generator']
                                
                                col_mat = box.column(align=True)
                                col_mat.label(text="Mapping :")
                                col_mat.prop(bark_node_group.inputs[1], 'default_value', text = "Scale")
                                col_mat.prop(bark_node_group.inputs[2], 'default_value', text = "Stretching")

                                col_mat = box.column(align=True)
                                col_mat.label(text="Color :")
                                col_mat.prop(bark_node_group.inputs[3], 'default_value', text = "Luminosity")
                                col_mat.prop(bark_node_group.inputs[4], 'default_value', text = "Contrast")
                                col_mat.prop(bark_node_group.inputs[5], 'default_value', text = "Saturation")
                                col_mat.prop(bark_node_group.inputs[6], 'default_value', text = "Color Contrast")
                                col_mat.separator(factor = 0.3)
                                col_mat.prop(bark_node_group.inputs[8], 'default_value', text = "Tint Intensity")
                                col_mat.prop(bark_node_group.inputs[7], 'default_value', text = "")
                                
                                col_mat = box.column(align=True)
                                col_mat.prop(bark_node_group.inputs[9], 'default_value', text = "Specular")
                                col_mat.prop(bark_node_group.inputs[10], 'default_value', text = "Specular Tint")
                                col_mat.prop(bark_node_group.inputs[11], 'default_value', text = "Roughness")
                                col_mat.prop(bark_node_group.inputs[12], 'default_value', text = "Bump")
                                col_mat.prop(bark_node_group.inputs[13], 'default_value', text = "Displacement")
                            else:
                                box.label(text="Custom material detected.")
                                box.operator("wm.url_open", text="Setup UV Mapping", icon = 'PLAY', depress = False).url = "https://youtu.be/4Juv1lC2pt0"
                        
                        else:
                            box.label(text="Set material.")
                        col.separator(factor = 2.5)


                    # EFFECTOR
                    if ivy_pref.panel_sub_effector == False:
                        col.separator(factor = 0.5)
                        col.prop(ivy_pref, 'panel_sub_effector', text = "Effector", emboss = False)
                        col.separator(factor = 1.5)
                    else:       
                        box = col.box()
                        box.prop(ivy_pref, 'panel_sub_effector', text = "Effector", emboss = False)
                        box.prop_search(ivy_modifier, '["Input_56"]', bpy.data, "collections", text="", icon="OUTLINER_COLLECTION")
                        row = box.row(align=True)
                        row.prop(ivy_modifier, '["Input_59"]', text="Distance")
                        box.operator('switch.buttonivy', text='Affect branches', depress = ivy_modifier["Input_60"]).index = "Input_60"
                        box.prop(ivy_modifier, '["Input_62"]', text = "Randomize Distance")
                        box.prop(ivy_modifier, '["Input_63"]', text = "Leaf Offset")

                        tips = row.operator("bagaivy.tooltips", text="", depress = False, icon = 'INFO')
                        tips.message = 'Select a mesh to use as an effector. Leaves and branches will be removed depending on the distance between the surface of your effector and the leaves. In the case of a window for example, your effector should be smaller than the window.'
                        tips.title = "Effector"
                        tips.image = "None"
                        tips.scale = 10
                        tips.url = "https://youtu.be/6x8FYzY5LnU"
                        row = box.row(align=True)
                        row.scale_y = 1.8
                        add = row.operator("ivyadd.target", text= "Add", icon = 'ADD')
                        add.index = 56
                        remove = row.operator("ivyremove.target", text= "Remove", icon = 'REMOVE')
                        remove.index = 56
                        col.separator(factor = 2.5)


                    # ANIMATION
                    if ivy_pref.panel_sub_animation == False:
                        col.separator(factor = 0.5)
                        col.prop(ivy_pref, 'panel_sub_animation', text = "Animation", emboss = False)
                        col.separator(factor = 1.5)
                    else:       
                        box = col.box()
                        box.prop(ivy_pref, 'panel_sub_animation', text = "Animation", emboss = False)
                        box.label(text = "Method :")
                        row = box.row(align=True)
                        row.operator('switch.buttonivy', depress = not ivy_modifier["Input_65"], text = "Continue").index = "Input_65"
                        row.operator('switch.buttonivy', depress = ivy_modifier["Input_65"], text = "Loop").index = "Input_65"

                        tips = row.operator("bagaivy.tooltips", text="", depress = False, icon = 'INFO')
                        tips.message = 'The "Continue" method creates a fluctuating wind, which is not uniform. The "Loop" method is for animations made to loop (every X frames the animation will repeat without the transition being visible)..'
                        tips.title = "Animation Method"
                        tips.image = "None"
                        tips.scale = 10
                        tips.url = "https://youtu.be/CKUn79qzYWM"

                        if ivy_modifier["Input_65"] == True:
                            box.prop(ivy_modifier, '["Input_68"]', text = "Loop every X frames")
                            box.prop(ivy_modifier, '["Input_67"]', text = "Speed")
                        else:
                            box.prop(ivy_modifier, '["Input_66"]', text = "Turbility")
                            box.prop(ivy_modifier, '["Input_69"]', text = "Speed")
                        
                        col_hv = box.column(align = True)
                        col_hv.label(text = "Vertical :")
                        col_hv.prop(ivy_modifier, '["Input_70"]', text = "Influence Texture")
                        col_hv.prop(ivy_modifier, '["Input_71"]', text = "Time Offset")
                        col_hv.prop(ivy_modifier, '["Input_72"]', text = "Intensity")
                        col_hv.prop(ivy_modifier, '["Input_73"]', text = "Random Intensity")
                        
                        col_hv = box.column(align = True)
                        col_hv.label(text = "Horizontal :")
                        col_hv.prop(ivy_modifier, '["Input_74"]', text = "Influence Texture")
                        col_hv.prop(ivy_modifier, '["Input_75"]', text = "Time Offset")
                        col_hv.prop(ivy_modifier, '["Input_76"]', text = "Intensity")
                        col_hv.prop(ivy_modifier, '["Input_77"]', text = "Random Intensity")
                        col.separator(factor = 2.5)


                    # GENERATION METHOD
                    if ivy_pref.panel_sub_method == False:
                        col.separator(factor = 0.5)
                        col.prop(ivy_pref, 'panel_sub_method', text = "Generation Method", emboss = False)
                        col.separator(factor = 1.5)
                    else:
                        box = col.box()
                        box.prop(ivy_pref, 'panel_sub_method', text = "Generation Method", emboss = False)
                        col_bis = box.column(align=True)
                        row = col_bis.row(align = True)
                        row.scale_y = 1.3
                        row.operator('switch.buttonivy', text='Snapping', depress = ivy_modifier["Input_4"]).index = "Input_4"
                        tips = row.operator("bagaivy.tooltips", text="", depress = False, icon = 'INFO')
                        tips.message = 'Snapping distance between suspended ivy and snapped ivy (on a wall/object). This settings is usefull in some precise cases such as complex targets or in case the ivy have to make a bridge between two points.'
                        tips.title = "Snapping"
                        tips.image = "None"
                        tips.scale = 10
                        tips.url = "None"
                        if ivy_modifier["Input_4"] == 1:
                            col_bis.prop(ivy_modifier, '["Input_7"]', text = "Distance")

                        
                        col_bis = box.column(align=True)
                        row = col_bis.row(align = True)
                        row.scale_y = 1.3
                        row.operator('switch.buttonivy', text='Displacement', depress = ivy_modifier["Input_5"]).index = "Input_5"
                        tips = row.operator("bagaivy.tooltips", text="", depress = False, icon = 'INFO')
                        tips.message = 'Add Noisy Displacement'
                        tips.title = "Displacement"
                        tips.image = "None"
                        tips.scale = 10
                        tips.url = "https://youtu.be/Vc6pcOZTV6Y"
                        if ivy_modifier["Input_5"] == 1:
                            col_bis.prop(ivy_modifier, '["Input_38"]', text = "Noise Scale")
                            col_bis.prop(ivy_modifier, '["Input_39"]', text = "Intensity")

                        
                        col_bis = box.column(align=True)
                        row = col_bis.row(align = True)
                        row.scale_y = 1.3
                        row.operator('switch.buttonivy', text='Offset', depress = ivy_modifier["Input_6"]).index = "Input_6"
                        tips = row.operator("bagaivy.tooltips", text="", depress = False, icon = 'INFO')
                        tips.message = 'The longer the branches will be, the more they will detach from the target.'
                        tips.title = "Offset"
                        tips.image = "None"
                        tips.scale = 10
                        tips.url = "https://youtu.be/EQDqBFd3cY8"
                        if ivy_modifier["Input_6"] == 1:
                            col_bis.prop(ivy_modifier, '["Input_37"]', text = "Displace")

                        
                        col_bis = box.column(align=True)
                        row = col_bis.row(align = True)
                        row.scale_y = 1.3
                        row.operator('switch.buttonivy', text='Decimate', depress = ivy_modifier["Input_50"]).index = "Input_50"
                        tips = row.operator("bagaivy.tooltips", text="", depress = False, icon = 'INFO')
                        tips.message = 'By default, branches are merged to reduce polycount at cost of realism, disable this option if you need more detail (for close-up).'
                        tips.title = "Decimate"
                        tips.image = "decimate"
                        tips.scale = 10
                        tips.url = "https://youtu.be/UmRxWGZWTYs"
                        col_bis.prop(ivy_modifier, '["Input_51"]', text = "Segment Length")

                        col.separator(factor = 2.5)


                    # VISIBILITY
                    if ivy_pref.panel_sub_visibility == False:
                        col.separator(factor = 0.5)
                        col.prop(ivy_pref, 'panel_sub_visibility', text = "Visibility", emboss = False)
                        col.separator(factor = 1.5)
                    else:
                        box = col.box()
                        box.prop(ivy_pref, 'panel_sub_visibility', text = "Visibility", emboss = False)
                        box.operator('switch.buttonivy', depress = not ivy_modifier["Input_26"], text = "Use leaf").index = "Input_26"
                        box.operator('switch.buttonivy', depress = ivy_modifier["Input_36"], text = "Use Flower").index = "Input_36"
                        row = box.row(align=True)
                        row.operator('switch.buttonivy', depress = ivy_modifier["Input_34"], text = "Use Proxy").index = "Input_34"
                        tips = row.operator("bagaivy.tooltips", text="", depress = False, icon = 'INFO')
                        tips.message = 'This option will create a low resolution of the ivy, only in the viewport. It will disapear in render.'
                        tips.title = "Orientation"
                        tips.image = "None"
                        tips.scale = 10
                        tips.url = "None"
                        box.operator('switch.buttonivy', depress = ivy_modifier["Input_40"], text = "Create Leaf Proxy").index = "Input_40"
                        col.separator(factor = 2.5)


                    # SOURCE OBJECTS
                    if ivy_pref.panel_sub_source_data == False:
                        col.separator(factor = 0.5)
                        col.prop(ivy_pref, 'panel_sub_source_data', text = "Source Objects", emboss = False)
                        col.separator(factor = 1.5)
                    else:
                        box = col.box()
                        box.prop(ivy_pref, 'panel_sub_source_data', text = "Source Objects", emboss = False)

                        box.label(text = "Targets :")
                        box.prop_search(ivy_modifier, '["Input_2"]', bpy.data, "collections", text="", icon="OUTLINER_COLLECTION")
                        box.label(text = "Start Points :")
                        box.prop_search(ivy_modifier, '["Input_3"]', bpy.data, "collections", text="", icon="OUTLINER_COLLECTION")
                        box.label(text = "Effectors :")                
                        box.prop_search(ivy_modifier, '["Input_56"]', bpy.data, "collections", text="", icon="OUTLINER_COLLECTION")


                        box.label(text = "Flowers Collection :")
                        row = box.row(align=True)
                        row.operator('switch.buttonivy', icon="OUTLINER_COLLECTION", depress = ivy_modifier["Input_19"], text = "").index = "Input_19"
                        row.operator('switch.buttonivy', icon = "OBJECT_DATA", depress = not ivy_modifier["Input_19"], text = "").index = "Input_19"
                        if ivy_modifier["Input_19"] == True:
                            row.prop_search(ivy_modifier, '["Input_21"]', bpy.data, "collections", text ="")
                        else:
                            row.prop_search(ivy_modifier, '["Input_20"]', bpy.data, "objects", text ="")


                        box.label(text = "Leaves Collection :")
                        row = box.row(align=True)
                        row.operator('switch.buttonivy', icon="OUTLINER_COLLECTION", depress = ivy_modifier["Input_22"], text = "").index = "Input_22"
                        row.operator('switch.buttonivy', icon = "OBJECT_DATA", depress = not ivy_modifier["Input_22"], text = "").index = "Input_22"
                        if ivy_modifier["Input_22"] == True:
                            row.prop_search(ivy_modifier, '["Input_24"]', bpy.data, "collections", text ="")
                        else:
                            row.prop_search(ivy_modifier, '["Input_23"]', bpy.data, "objects", text ="")

                        box.label(text = "Assets Rotation Offset:")
                        row = box.row(align=True)
                        row.prop(ivy_modifier, '["Input_43"]', text="")
                        tips = row.operator("bagaivy.tooltips", text="", depress = False, icon = 'INFO')
                        tips.message = 'Assets should be +Y oriented. If this is not the case, you can correct the rotation here.'
                        tips.title = "Orientation"
                        tips.image = "None"
                        tips.scale = 10
                        tips.url = "None"
                        col.separator(factor = 2.5)


                ###################################################################################
                # FAST
                ###################################################################################  
                elif ivy_modifier["Input_81"]:

                    # IVY ABOUT MODE
                    if ivy_pref.panel_sub_about == False:
                        col.prop(ivy_pref, 'panel_sub_about', text = "About Fast mode", emboss = True, icon = "TRIA_RIGHT")
                    else:
                        box = col.box()
                        box.prop(ivy_pref, 'panel_sub_about', text = "About Fast mode :", emboss = False, icon = "TRIA_DOWN")
                        col_about = box.column(align=True)
                        col_about.scale_y=0.8
                        text = "Generate ivy by drawing on your target's surface. The generated ivy is designed for quick computation at the expense of precision."
                        lines = split_text(text, 28)
                        for line in lines: col_about.label(text=line)
                        col_about.separator(factor = 1)
                        text = "This generator creates an initial 'piece' of ivy and replicates it around the drawn areas."
                        lines = split_text(text, 28)
                        for line in lines: col_about.label(text=line)
                        col_about.separator(factor = 1)
                        text = "We recommend using this ivy for backgrounds, large surfaces or in the secondary scene."
                        lines = split_text(text, 28)
                        for line in lines: col_about.label(text=line)

                    if bpy.context.object.mode == 'OBJECT':
                        cobox = col.box().column(align=True)
                        if ivy_modifier["Input_120"] != "":
                            cobox.label(text = ' '.join(word.capitalize() for word in ivy_modifier["Input_120"].split('_')))
                        row = cobox.row(align=True)
                        row.scale_y = 2
                        row.operator("ivy.replace_preset", text = "Replace Presets")
                        tips = row.operator("bagaivy.tooltips", text="", emboss = True, depress = False, icon = 'INFO')
                        tips.message = 'You can select another preset in the asset browser to replace the current ivy. Any changes you may have made to this ivy will not be saved.'
                        tips.title = "Replace Presets"
                        tips.image = "None"
                        tips.scale = 10
                        tips.url = "None"
                    col.separator(factor = 1.5)


                    # IVY GROWTH
                    if ivy_pref.panel_sub_distribution == False:
                        col.separator(factor = 0.5)
                        col.prop(ivy_pref, 'panel_sub_distribution', text = "Ivy Growth", emboss = False)
                        col.separator(factor = 1.5)
                    else:
                        box = col.box()
                        box.prop(ivy_pref, 'panel_sub_distribution', text = "Ivy Growth", emboss = False)

                        box.prop(ivy_modifier, '["Input_108"]', text="Ivy Density")
                        box.prop(ivy_modifier, '["Input_109"]', text="Ivy Propagation")
                        box.prop(ivy_modifier, '["Input_104"]', text="Angle Target Edge")
                        box.label(text = "Ivy Bridge")
                        row = box.row(align = True)
                        row.prop(ivy_modifier, '["Input_111"]', text="Drop Min")
                        row.prop(ivy_modifier, '["Input_112"]', text="Drop Max")
                        box.prop(ivy_modifier, '["Input_110"]', text="Bridge Count")
                        
                        if bpy.context.object.mode == 'OBJECT':

                            subcoll = box.column(align=True)
                            row = subcoll.row(align=True)
                            row.label(text="Target")
                            tips = row.operator("bagaivy.tooltips", text="", emboss = False, depress = False, icon = 'INFO')
                            tips.message = 'Ivy needs to know what surface it can grow on. Easily add or remove objects to grow on.'
                            tips.title = "Ivy target"
                            tips.image = "None"
                            tips.scale = 10
                            tips.url = "https://youtu.be/dh9fl1J59yo"
                            row = subcoll.row(align=True)
                            row.scale_y = 1.8
                            add = row.operator("ivyadd.target", text= "Add", icon = 'ADD')
                            add.index = 2
                            remove = row.operator("ivyremove.target", text= "Remove", icon = 'REMOVE')
                            remove.index = 2


                    # ISLAND
                    if ivy_pref.panel_sub_island == False:
                        col.separator(factor = 0.5)
                        col.prop(ivy_pref, 'panel_sub_island', text = "Ivy Island", emboss = False)
                        col.separator(factor = 1.5)
                    else:
                        box = col.box()
                        box.prop(ivy_pref, 'panel_sub_island', text = "Ivy Island", emboss = False)
                        col_doii = box.column()
                        col_doii.scale_y = 2
                        col_doii.operator('switch.buttonivy', depress = ivy_modifier["Input_95"], text = "Display only ivy island").index = "Input_95"
                        if ivy_modifier["Input_95"]:
                            box.label(text="Ivy displayed at World Origin")

                        # Branch
                        box_br = box.box().column(align=True)
                        box_br.label(text = "Branch")
                        box_br.prop(ivy_modifier, '["Input_98"]', text="Amount")
                        box_br.prop(ivy_modifier, '["Input_101"]', text="Branch Length")
                        box_br.prop(ivy_modifier, '["Input_178"]', text="Segment Length")
                        box_br.prop(ivy_modifier, '["Input_91"]', text="Resolution")
                        box_br.prop(ivy_modifier, '["Input_102"]', text="Random Growth Offset")
                        box_br.separator(factor = 0.3)
                        box_br.label(text = "Wavy Growth")
                        box_br.prop(ivy_modifier, '["Input_96"]', text="Intensity")
                        box_br.prop(ivy_modifier, '["Input_115"]', text="Scale")
                        box_br.prop(ivy_modifier, '["Input_103"]', text="Z-Noise Intensity")
                        box_br.separator(factor = 0.3)
                        box_br.label(text = "Branch Detachment")
                        box_br.prop(ivy_modifier, '["Input_99"]', text="Offset")
                        box_br.prop(ivy_modifier, '["Input_100"]', text="Randomize")
                        box_br.prop(ivy_modifier, '["Input_116"]', text="Scale")

                        subcoll = box.column(align=True)
                        subcoll.label(text = "Branch Radius")
                        row = subcoll.row(align = True)
                        row.prop(ivy_modifier, '["Input_90"]', text="Min")
                        row.prop(ivy_modifier, '["Input_113"]', text="Max")
                        # Leaf
                        # box_lf = box.box().column(align=True)
                        # box_lf.label(text = "Leaves")
                        # box_lf.prop(ivy_modifier, '["Input_92"]', text="Leaf Density")
                        # box_lf.prop(ivy_modifier, '["Input_97"]', text="Leaf Opening Alternation")
                        


                        box.prop(ivy_modifier, '["Input_105"]', text="Seed")


                    # LEAVES
                    if ivy_pref.panel_sub_leaf == False:
                        col.separator(factor = 0.5)
                        col.prop(ivy_pref, 'panel_sub_leaf', text = "Leaves", emboss = False)
                        col.separator(factor = 1.5)
                    else:
                        box = col.box()
                        box.prop(ivy_pref, 'panel_sub_leaf', text = "Leaves", emboss = False)
                        col_new = box.column(align=True)
                        col_new.prop(ivy_modifier, '["Input_92"]', text="Leaves Density")

                        subcoll = box.column(align=True)
                        subcoll.label(text = "Leaves Random Scale :")
                        row = subcoll.row(align = True)
                        row.prop(ivy_modifier, '["Input_93"]', text="Min")
                        row.prop(ivy_modifier, '["Input_94"]', text="Max")
                        
                        col_two=box.column(align=True)
                        row = col_two.row(align=True)
                        row.scale_y = 1.8
                        add = row.operator("ivyadd.asset", text= "Add Leaf", icon = 'ADD')
                        add.index = 24

                        row = col_two.row(align=True)
                        row.scale_y = 0.9
                        row.label(text="Source :")
                        row.prop(ivy_pref, 'panel_asset_source', text = "View 3D",  toggle = True)
                        row.prop(ivy_pref, 'panel_asset_source', text = "Asset Browser",  toggle = True, invert_checkbox=True)

                        col_two.separator(factor = 0.6)
                        row = col_two.row(align=True)
                        row.scale_y = 1.8
                        remove = row.operator("ivyremove.asset", text= "Remove Leaf", icon = 'REMOVE')
                        remove.index = 24

                        box = box.box()
                        box.prop(ivy_pref, 'panel_sub_leaf_avanced', text = "Advanced ", emboss = True)
                        if ivy_pref.panel_sub_leaf_avanced == True:
                            box.prop(ivy_modifier, '["Input_97"]', text="Alternating rotation")
                            box.prop(ivy_modifier, '["Input_117"]', text="Random Rotation")

                            box.label(text = "Inclination :")
                            row = box.row(align = True)
                            row.prop(ivy_modifier, '["Input_118"]', text="Min")
                            row.prop(ivy_modifier, '["Input_119"]', text="Max")
                            box.prop(ivy_modifier, '["Input_79"]', text="Offset Leaves Local")
                            box.prop(ivy_modifier, '["Input_55"]', text="Rotation Local")
                            box.prop(ivy_modifier, '["Input_88"]', text="Align Z Global")
                            
                        if ivy_modifier["Input_26"] == True:
                            col_tree=box.column(align=True)
                            col_tree.alert = True
                            col_tree.label(text="Leaf are disabled :")
                            col_tree.operator('switch.buttonivy', depress = ivy_modifier["Input_26"], text = "Use Leaf", icon = 'ERROR').index = "Input_26"
                        col.separator(factor = 2.5)


                    # FLOWERS
                    if ivy_pref.panel_sub_flower == False:
                        col.separator(factor = 0.5)
                        col.prop(ivy_pref, 'panel_sub_flower', text = "Flowers/Fruits", emboss = False)
                        col.separator(factor = 1.5)
                    else:
                        box = col.box()
                        box.prop(ivy_pref, 'panel_sub_flower', text = "Flowers/Fruits", emboss = False)
                        col_new = box.column(align=True)
                        box.prop(ivy_modifier, '["Input_168"]', text="Animation")
                        col_new.prop(ivy_modifier, '["Input_84"]', text="Probability per Island")

                        box.label(text = "Flowers Random Scale :")
                        row = box.row(align = True)
                        row.prop(ivy_modifier, '["Input_41"]', text="Min")
                        row.prop(ivy_modifier, '["Input_42"]', text="Max")
                        
                        box.label(text = "Flowers Branch Alignment :")
                        row = box.row(align = True)
                        row.prop(ivy_modifier, '["Input_106"]', text="Start")
                        row.prop(ivy_modifier, '["Input_107"]', text="End")
                        
                        
                        col_two=box.column(align=True)
                        row = col_two.row(align=True)
                        row.scale_y = 1.8
                        add = row.operator("ivyadd.asset", text= "Add Flower", icon = 'ADD')
                        add.index = 21

                        row = col_two.row(align=True)
                        row.scale_y = 0.9
                        row.label(text="Source :")
                        row.prop(ivy_pref, 'panel_asset_source', text = "View 3D",  toggle = True)
                        row.prop(ivy_pref, 'panel_asset_source', text = "Asset Browser",  toggle = True, invert_checkbox=True)

                        col_two.separator(factor = 0.6)
                        row = col_two.row(align=True)
                        row.scale_y = 1.8
                        remove = row.operator("ivyremove.asset", text= "Remove Flower", icon = 'REMOVE')
                        remove.index = 21

                        if ivy_modifier["Input_36"] == False:
                            col_tree=box.column(align=True)
                            col_tree.alert = True
                            col_tree.label(text="Flowers are disabled :")
                            col_tree.operator('switch.buttonivy', depress = ivy_modifier["Input_36"], text = "Use Flower", icon = 'ERROR').index = "Input_36"
                                
                        box = box.box()
                        row = box.row(align=True)
                        row.prop(ivy_pref, 'panel_sub_flower_avanced', text = "Advanced ", emboss = True)
                        tips = row.operator("bagaivy.tooltips", text="", depress = False, icon = 'INFO', emboss = False)
                        tips.message = 'Parameters : Alternating Rotation, Random Rotation and Inclination are common between leaves and flowers. You can set them in the Leaves panel.'
                        tips.title = "Animation Method"
                        tips.image = "None"
                        tips.scale = 10
                        tips.url = "None"
                        if ivy_pref.panel_sub_flower_avanced == True:
                            box.prop(ivy_modifier, '["Input_78"]', text="Offset Flower Local")
                            box.prop(ivy_modifier, '["Input_194"]', text="Rotation Local")
                            box.prop(ivy_modifier, '["Input_89"]', text="Align Z Ivy Island")
                        col.separator(factor = 2.5)


                    # TRUNK
                    if ivy_pref.panel_sub_trunk == False:
                        col.separator(factor = 0.5)
                        col.prop(ivy_pref, 'panel_sub_trunk', text = "Trunk", emboss = False)
                        col.separator(factor = 1.5)
                    else:
                        box = col.box()
                        box.prop(ivy_pref, 'panel_sub_trunk', text = "Trunk", emboss = False)
                        box.operator('switch.buttonivy', depress = ivy_modifier["Input_114"], text = "Use Trunk").index = "Input_114"

                        box.label(text="Material :")
                        row = box.row(align=True)
                        row.prop_search(ivy_modifier, '["Input_48"]', bpy.data, "materials", text="", icon="MATERIAL")

                        tips = row.operator("bagaivy.tooltips", text="", depress = False, icon = 'INFO')
                        tips.message = 'You can set any shader here. If you use the default shader it will be displayed here. UVs are created by default, you can use them in your own shader by using the Attribute node with the attribute "UVs".'
                        tips.title = "Material"
                        tips.image = "None"
                        tips.scale = 10
                        tips.url = "None"

                        bark_mat = ivy_modifier['Input_48']
                        if bark_mat is not None:
                            if bark_mat.name.startswith('BIG_Ivy_Bark'):
                                bark_node_group = bark_mat.node_tree.nodes['BIG_Ivy_Bark_Generator']
                                
                                col_mat = box.column(align=True)
                                col_mat.label(text="Mapping :")
                                col_mat.prop(bark_node_group.inputs[1], 'default_value', text = "Scale")
                                col_mat.prop(bark_node_group.inputs[2], 'default_value', text = "Stretching")

                                col_mat = box.column(align=True)
                                col_mat.label(text="Color :")
                                col_mat.prop(bark_node_group.inputs[3], 'default_value', text = "Luminosity")
                                col_mat.prop(bark_node_group.inputs[4], 'default_value', text = "Contrast")
                                col_mat.prop(bark_node_group.inputs[5], 'default_value', text = "Saturation")
                                col_mat.prop(bark_node_group.inputs[6], 'default_value', text = "Color Contrast")
                                col_mat.separator(factor = 0.3)
                                col_mat.prop(bark_node_group.inputs[8], 'default_value', text = "Tint Intensity")
                                col_mat.prop(bark_node_group.inputs[7], 'default_value', text = "")
                                
                                col_mat = box.column(align=True)
                                col_mat.prop(bark_node_group.inputs[9], 'default_value', text = "Specular")
                                col_mat.prop(bark_node_group.inputs[10], 'default_value', text = "Specular Tint")
                                col_mat.prop(bark_node_group.inputs[11], 'default_value', text = "Roughness")
                                col_mat.prop(bark_node_group.inputs[12], 'default_value', text = "Bump")
                                col_mat.prop(bark_node_group.inputs[13], 'default_value', text = "Displacement")
                            else:
                                box.label(text="Custom material detected.")
                                box.operator("wm.url_open", text="Setup UV Mapping", icon = 'PLAY', depress = False).url = "https://youtu.be/4Juv1lC2pt0"
                        
                        else:
                            box.label(text="Set material.")
                        col.separator(factor = 2.5)


                    # EFFECTOR
                    if ivy_pref.panel_sub_effector == False:
                        col.separator(factor = 0.5)
                        col.prop(ivy_pref, 'panel_sub_effector', text = "Effector", emboss = False)
                        col.separator(factor = 1.5)
                    else:
                        box = col.box()
                        box.prop(ivy_pref, 'panel_sub_effector', text = "Effector", emboss = False)
                        box.prop_search(ivy_modifier, '["Input_56"]', bpy.data, "collections", text="", icon="OUTLINER_COLLECTION")
                        row = box.row(align=True)
                        row.prop(ivy_modifier, '["Input_59"]', text="Distance")
                        box.prop(ivy_modifier, '["Input_62"]', text = "Randomize Distance")

                        tips = row.operator("bagaivy.tooltips", text="", depress = False, icon = 'INFO')
                        tips.message = 'Select a mesh to use as an effector. Leaves and branches will be removed depending on the distance between the surface of your effector and the leaves. In the case of a window for example, your effector should be smaller than the window.'
                        tips.title = "Effector"
                        tips.image = "None"
                        tips.scale = 10
                        tips.url = "https://youtu.be/6x8FYzY5LnU"
                        row = box.row(align=True)
                        row.scale_y = 1.8
                        add = row.operator("ivyadd.target", text= "Add", icon = 'ADD')
                        add.index = 56
                        remove = row.operator("ivyremove.target", text= "Remove", icon = 'REMOVE')
                        remove.index = 56
                        col.separator(factor = 2.5)


                    # ANIMATION
                    if ivy_pref.panel_sub_animation == False:
                        col.separator(factor = 0.5)
                        col.prop(ivy_pref, 'panel_sub_animation', text = "Animation", emboss = False)
                        col.separator(factor = 1.5)
                    else:
                        box = col.box()
                        box.prop(ivy_pref, 'panel_sub_animation', text = "Animation", emboss = False)
                        box.label(text = "Method :")
                        row = box.row(align=True)
                        row.operator('switch.buttonivy', depress = not ivy_modifier["Input_65"], text = "Continue").index = "Input_65"
                        row.operator('switch.buttonivy', depress = ivy_modifier["Input_65"], text = "Loop").index = "Input_65"

                        tips = row.operator("bagaivy.tooltips", text="", depress = False, icon = 'INFO')
                        tips.message = 'The "Continue" method creates a fluctuating wind, which is not uniform. The "Loop" method is for animations made to loop (every X frames the animation will repeat without the transition being visible)..'
                        tips.title = "Animation Method"
                        tips.image = "None"
                        tips.scale = 10
                        tips.url = "https://youtu.be/CKUn79qzYWM"

                        if ivy_modifier["Input_65"] == True:
                            box.prop(ivy_modifier, '["Input_68"]', text = "Loop every X frames")
                            box.prop(ivy_modifier, '["Input_67"]', text = "Speed")
                        else:
                            box.prop(ivy_modifier, '["Input_66"]', text = "Turbility")
                            box.prop(ivy_modifier, '["Input_69"]', text = "Speed")
                        
                        col_hv = box.column(align = True)
                        col_hv.label(text = "Vertical :")
                        col_hv.prop(ivy_modifier, '["Input_70"]', text = "Influence Texture")
                        col_hv.prop(ivy_modifier, '["Input_71"]', text = "Time Offset")
                        col_hv.prop(ivy_modifier, '["Input_72"]', text = "Intensity")
                        col_hv.prop(ivy_modifier, '["Input_73"]', text = "Random Intensity")
                        
                        col_hv = box.column(align = True)
                        col_hv.label(text = "Horizontal :")
                        col_hv.prop(ivy_modifier, '["Input_74"]', text = "Influence Texture")
                        col_hv.prop(ivy_modifier, '["Input_75"]', text = "Time Offset")
                        col_hv.prop(ivy_modifier, '["Input_76"]', text = "Intensity")
                        col_hv.prop(ivy_modifier, '["Input_77"]', text = "Random Intensity")
                        col.separator(factor = 2.5)


                    # VISIBILITY
                    if ivy_pref.panel_sub_visibility == False:
                        col.separator(factor = 0.5)
                        col.prop(ivy_pref, 'panel_sub_visibility', text = "Visibility", emboss = False)
                        col.separator(factor = 1.5)
                    else:
                        box = col.box()
                        box.prop(ivy_pref, 'panel_sub_visibility', text = "Visibility", emboss = False)
                        box.operator('switch.buttonivy', depress = not ivy_modifier["Input_26"], text = "Use leaf").index = "Input_26"
                        box.operator('switch.buttonivy', depress = ivy_modifier["Input_36"], text = "Use Flower").index = "Input_36"
                        box.operator('switch.buttonivy', depress = ivy_modifier["Input_114"], text = "Use Trunk").index = "Input_114"
                        row = box.row(align=True)
                        row.operator('switch.buttonivy', depress = ivy_modifier["Input_34"], text = "Use Proxy").index = "Input_34"
                        tips = row.operator("bagaivy.tooltips", text="", depress = False, icon = 'INFO')
                        tips.message = 'This option will create a low resolution of the ivy, only in the viewport. It will disapear in render.'
                        tips.title = "Orientation"
                        tips.image = "None"
                        tips.scale = 10
                        tips.url = "None"
                        box.operator('switch.buttonivy', depress = ivy_modifier["Input_40"], text = "Create Leaf Proxy").index = "Input_40"
                        col.separator(factor = 2.5)


                    # SOURCE OBJECTS
                    if ivy_pref.panel_sub_source_data == False:
                        col.separator(factor = 0.5)
                        col.prop(ivy_pref, 'panel_sub_source_data', text = "Source Objects", emboss = False)
                        col.separator(factor = 1.5)
                    else:
                        box = col.box()
                        box.prop(ivy_pref, 'panel_sub_source_data', text = "Source Objects", emboss = False)

                        box.label(text = "Targets :")
                        box.prop_search(ivy_modifier, '["Input_2"]', bpy.data, "collections", text="", icon="OUTLINER_COLLECTION")
                        box.label(text = "Start Points :")
                        box.prop_search(ivy_modifier, '["Input_3"]', bpy.data, "collections", text="", icon="OUTLINER_COLLECTION")
                        box.label(text = "Effectors :")                
                        box.prop_search(ivy_modifier, '["Input_56"]', bpy.data, "collections", text="", icon="OUTLINER_COLLECTION")


                        box.label(text = "Flowers Collection :")
                        row = box.row(align=True)
                        row.operator('switch.buttonivy', icon="OUTLINER_COLLECTION", depress = ivy_modifier["Input_19"], text = "").index = "Input_19"
                        row.operator('switch.buttonivy', icon = "OBJECT_DATA", depress = not ivy_modifier["Input_19"], text = "").index = "Input_19"
                        if ivy_modifier["Input_19"] == True:
                            row.prop_search(ivy_modifier, '["Input_21"]', bpy.data, "collections", text ="")
                        else:
                            row.prop_search(ivy_modifier, '["Input_20"]', bpy.data, "objects", text ="")


                        box.label(text = "Leaves Collection :")
                        row = box.row(align=True)
                        row.operator('switch.buttonivy', icon="OUTLINER_COLLECTION", depress = ivy_modifier["Input_22"], text = "").index = "Input_22"
                        row.operator('switch.buttonivy', icon = "OBJECT_DATA", depress = not ivy_modifier["Input_22"], text = "").index = "Input_22"
                        if ivy_modifier["Input_22"] == True:
                            row.prop_search(ivy_modifier, '["Input_24"]', bpy.data, "collections", text ="")
                        else:
                            row.prop_search(ivy_modifier, '["Input_23"]', bpy.data, "objects", text ="")

                        box.label(text = "Assets Rotation Offset:")
                        row = box.row(align=True)
                        row.prop(ivy_modifier, '["Input_43"]', text="")
                        tips = row.operator("bagaivy.tooltips", text="", depress = False, icon = 'INFO')
                        tips.message = 'Assets should be +Y oriented. If this is not the case, you can correct the rotation here.'
                        tips.title = "Orientation"
                        tips.image = "None"
                        tips.scale = 10
                        tips.url = "None"
                        col.separator(factor = 2.5)


                ###################################################################################
                # PRECISION
                ###################################################################################  
                elif ivy_modifier["Input_83"]:

                    # IVY ABOUT MODE
                    if ivy_pref.panel_sub_about == False:
                        col.prop(ivy_pref, 'panel_sub_about', text = "About Fast mode", emboss = True, icon = "TRIA_RIGHT")
                    else:
                        box = col.box()
                        box.prop(ivy_pref, 'panel_sub_about', text = "About Fast mode :", emboss = False, icon = "TRIA_DOWN")
                        col_about = box.column(align=True)
                        col_about.scale_y=0.8
                        text = "Generate ivy branch by branch through drawing. You have the ability to manually adjust the radius and tilt of each branch."
                        lines = split_text(text, 28)
                        for line in lines: col_about.label(text=line)
                        col_about.separator(factor = 1)
                        text = "This generator is designed for manual editing and does not produce branch ramifications."
                        lines = split_text(text, 28)
                        for line in lines: col_about.label(text=line)
                        col_about.separator(factor = 1)
                        text = "We recommend using this for foreground elements, or whenever you require precision in the propagation and positioning of the ivy."
                        lines = split_text(text, 28)
                        for line in lines: col_about.label(text=line)

                    if bpy.context.object.mode == 'OBJECT':
                        cobox = col.box().column(align=True)
                        if ivy_modifier["Input_120"] != "":
                            cobox.label(text = ' '.join(word.capitalize() for word in ivy_modifier["Input_120"].split('_')))
                        row = cobox.row(align=True)
                        row.scale_y = 2
                        row.operator("ivy.replace_preset", text = "Replace Presets")
                        tips = row.operator("bagaivy.tooltips", text="", emboss = True, depress = False, icon = 'INFO')
                        tips.message = 'You can select another preset in the asset browser to replace the current ivy. Any changes you may have made to this ivy will not be saved.'
                        tips.title = "Replace Presets"
                        tips.image = "None"
                        tips.scale = 10
                        tips.url = "None"
                    col.separator(factor = 1.5)

                    # IVY GROWTH
                    if ivy_pref.panel_sub_distribution == False:
                        col.separator(factor = 0.5)
                        col.prop(ivy_pref, 'panel_sub_distribution', text = "Ivy Branch", emboss = False)
                        col.separator(factor = 1.5)
                    else:
                        box = col.box()
                        box.prop(ivy_pref, 'panel_sub_distribution', text = "Ivy Branch", emboss = False)

                        col2 = box.column(align=True)
                        col2.prop(ivy_modifier, '["Input_85"]', text="Resolution")        
                        row = col2.row(align = True)                
                        row.operator('switch.buttonivy', depress = not ivy_modifier["Input_132"], text = "Auto Snap").index = "Input_132"
                        tips = row.operator("bagaivy.tooltips", text="", emboss = True, depress = False, icon = 'INFO')
                        tips.message = "By enabling Auto Snap, nearby branches will merge. However, radius adjustment (Alt+S) will still be required."
                        tips.title = "Auto Snap"
                        tips.image = "None"
                        tips.scale = 10
                        tips.url = "None"
                        if ivy_modifier["Input_132"] == False:
                            col2.prop(ivy_modifier, '["Input_121"]', text="Snapping Distance")

                        col2 = box.column(align=True)
                        row = col2.row(align = True)
                        row.label(text = "Deform along Z")
                        tips = row.operator("bagaivy.tooltips", text="", emboss = False, depress = False, icon = 'INFO')
                        tips.message = "Distort the branch according to the normal of the nearest target face."
                        tips.title = "Auto Snap"
                        tips.image = "None"
                        tips.scale = 10
                        tips.url = "None"
                        col2.prop(ivy_modifier, '["Input_123"]', text="Intensity")
                        col2.prop(ivy_modifier, '["Input_125"]', text="Scale")
                        row = col2.row(align = True)
                        row.prop(ivy_modifier, '["Input_124"]', text="Distance", icon = 'LINKED')
                        tips = row.operator("bagaivy.tooltips", text="", emboss = True, depress = False, icon = 'INFO')
                        tips.message = "This value ensures that beyond a certain distance from the target surface, this deformation is no longer present."
                        tips.title = "Deformation"
                        tips.image = "None"
                        tips.scale = 10
                        tips.url = "None"

                        col2 = box.column(align=True)
                        col2.label(text = "Deform along XY")
                        col2.prop(ivy_modifier, '["Input_126"]', text="Scale")
                        col2.prop(ivy_modifier, '["Input_127"]', text="Intensity")

                        col2 = box.column(align=True)
                        col2.label(text = "Deform Global")
                        col2.prop(ivy_modifier, '["Input_128"]', text="Intensity")
                        col2.prop(ivy_modifier, '["Input_129"]', text="Scale")
                        row = col2.row(align = True)
                        row.prop(ivy_modifier, '["Input_124"]', text="Distance", icon = 'LINKED')
                        tips = row.operator("bagaivy.tooltips", text="", emboss = True, depress = False, icon = 'INFO')
                        tips.message = "This value determines the distance from the target surface at which this deformation begins."
                        tips.title = "Deformation"
                        tips.image = "None"
                        tips.scale = 10
                        tips.url = "None"

                        col2 = box.column(align=True)
                        col2.prop(ivy_modifier, '["Input_130"]', text="Twist")
                        col2.prop(ivy_modifier, '["Input_131"]', text="Spiral")

                        box.prop(ivy_modifier, '["Input_187"]', text="Seed")
                        
                        
                        if bpy.context.object.mode == 'OBJECT':

                            subcoll = box.column(align=True)
                            row = subcoll.row(align=True)
                            row.label(text="Target")
                            tips = row.operator("bagaivy.tooltips", text="", emboss = False, depress = False, icon = 'INFO')
                            tips.message = 'Ivy needs to know what surface it can grow on. Easily add or remove objects to grow on.'
                            tips.title = "Ivy target"
                            tips.image = "None"
                            tips.scale = 10
                            tips.url = "https://youtu.be/dh9fl1J59yo"
                            row = subcoll.row(align=True)
                            row.scale_y = 1.8
                            add = row.operator("ivyadd.target", text= "Add", icon = 'ADD')
                            add.index = 2
                            remove = row.operator("ivyremove.target", text= "Remove", icon = 'REMOVE')
                            remove.index = 2

                        col.separator(factor = 1.5)


                    # LEAVES
                    if ivy_pref.panel_sub_leaf == False:
                        col.separator(factor = 0.5)
                        col.prop(ivy_pref, 'panel_sub_leaf', text = "Leaves", emboss = False)
                        col.separator(factor = 1.5)
                    else:
                        box = col.box()
                        box.prop(ivy_pref, 'panel_sub_leaf', text = "Leaves", emboss = False)

                        box.prop(ivy_modifier, '["Input_171"]', text="Density")
                        tips = box.operator("bagaivy.tooltips", text="Tips !", emboss = True, depress = False, icon = 'INFO')
                        tips.message = "End/Start values control the branch thickness from its start (where it's thickest = Start) to its end (where it's thinnest = End). Tweaking End, for instance, influences the leaves at the branch's end, with farther leaves being less affected."
                        tips.title = "End / Start values"
                        tips.image = "None"
                        tips.scale = 10
                        tips.url = "None"

                        col2 = box.column(align=True)
                        col2.label(text = "Density Radius Based")
                        row = col2.row(align = True)
                        row.prop(ivy_modifier, '["Input_176"]', text="End")
                        row.prop(ivy_modifier, '["Input_177"]', text="Start")

                        col2 = box.column(align=True)
                        col2.label(text = "Align to Branch")
                        row = col2.row(align = True)
                        row.prop(ivy_modifier, '["Input_175"]', text="Start")
                        row.prop(ivy_modifier, '["Input_174"]', text="End")
                        row.prop(ivy_modifier, '["Input_206"]', text="", icon ="ARROW_LEFTRIGHT")

                        col2 = box.column(align=True)
                        col2.label(text = "Align to Ground (-Z)")
                        row = col2.row(align = True)
                        row.prop(ivy_modifier, '["Input_183"]', text="Start")
                        row.prop(ivy_modifier, '["Input_181"]', text="End")
                        row.prop(ivy_modifier, '["Input_207"]', text="", icon ="ARROW_LEFTRIGHT")

                        col2 = box.column(align=True)
                        row = col2.row(align = True)
                        split = row.split(factor=0.6)
                        split.label(text = "Align to Target")
                        rowsp = split.row(align = True)
                        rowsp.prop(ivy_modifier, '["Input_208"]', invert_checkbox = True, text="Y")
                        rowsp.prop(ivy_modifier, '["Input_208"]', text="Z")
                        row = col2.row(align = True)
                        row.prop(ivy_modifier, '["Input_189"]', text="Start")
                        row.prop(ivy_modifier, '["Input_188"]', text="End")
                        row.prop(ivy_modifier, '["Input_209"]', text="", icon ="ARROW_LEFTRIGHT")
                        col2.prop(ivy_modifier, '["Input_190"]', text="Distance max")

                        col2 = box.column(align=True)
                        col2.label(text = "Rotation Local X")
                        row = col2.row(align = True)
                        row.prop(ivy_modifier, '["Input_143"]', text="End")
                        row.prop(ivy_modifier, '["Input_144"]', text="Start")
                        col2.prop(ivy_modifier, '["Input_145"]', text="Random")

                        col2 = box.column(align=True)
                        col2.label(text = "Rotation Local Y")
                        row = col2.row(align = True)
                        row.prop(ivy_modifier, '["Input_146"]', text="End")
                        row.prop(ivy_modifier, '["Input_147"]', text="Start")
                        col2.prop(ivy_modifier, '["Input_180"]', text="Random")

                        col2 = box.column(align=True)
                        col2.label(text = "Rotation Local Z")
                        row = col2.row(align = True)
                        row.prop(ivy_modifier, '["Input_149"]', text="End")
                        row.prop(ivy_modifier, '["Input_150"]', text="Start")
                        col2.prop(ivy_modifier, '["Input_151"]', text="Random")

                        col2 = box.column(align=True)
                        col2.label(text = "Scale")
                        row = col2.row(align = True)
                        row.prop(ivy_modifier, '["Input_152"]', text="End")
                        row.prop(ivy_modifier, '["Input_153"]', text="Start")
                        col2.prop(ivy_modifier, '["Input_154"]', text="Random")

                        box.prop(ivy_modifier, '["Input_192"]', text="Local Offset")

                        box.prop(ivy_modifier, '["Input_187"]', text="Seed")
                        
                        col_two=box.column(align=True)
                        row = col_two.row(align=True)
                        row.scale_y = 1.8
                        add = row.operator("ivyadd.asset", text= "Add Leaf", icon = 'ADD')
                        add.index = 24

                        row = col_two.row(align=True)
                        row.scale_y = 0.9
                        row.label(text="Source :")
                        row.prop(ivy_pref, 'panel_asset_source', text = "View 3D",  toggle = True)
                        row.prop(ivy_pref, 'panel_asset_source', text = "Asset Browser",  toggle = True, invert_checkbox=True)

                        col_two.separator(factor = 0.6)
                        row = col_two.row(align=True)
                        row.scale_y = 1.8
                        remove = row.operator("ivyremove.asset", text= "Remove Leaf", icon = 'REMOVE')
                        remove.index = 24


                    # FLOWERS
                    if ivy_pref.panel_sub_flower == False:
                        col.separator(factor = 0.5)
                        col.prop(ivy_pref, 'panel_sub_flower', text = "Flowers/Fruits", emboss = False)
                        col.separator(factor = 1.5)
                    else:
                        box = col.box()
                        box.prop(ivy_pref, 'panel_sub_flower', text = "Flowers/Fruits", emboss = False)

                        if ivy_modifier["Input_36"] == False:
                            col_tree=box.column(align=True)
                            col_tree.alert = True
                            col_tree.label(text="Flowers are disabled :")
                            col_tree.operator('switch.buttonivy', depress = ivy_modifier["Input_36"], text = "Use Flower", icon = 'ERROR').index = "Input_36"
                                
                        box.prop(ivy_modifier, '["Input_122"]', text="Flowers Probability")
                        col2 = box.column(align=True)
                        row = col2.row(align = True)
                        row.prop(ivy_modifier, '["Input_168"]', text="Animation")
                        tips = row.operator("bagaivy.tooltips", text="", emboss = True, depress = False, icon = 'INFO')
                        tips.message = "Toggle to gradually stop flower/fruit animation (1=On and 0=Off)"
                        tips.title = "Flowers & Fruits Animation"
                        tips.image = "None"
                        tips.scale = 10
                        tips.url = "None"

                        col2 = box.column(align=True)
                        col2.label(text = "Align to Branch")
                        row = col2.row(align = True)
                        row.prop(ivy_modifier, '["Input_186"]', text="Start")
                        row.prop(ivy_modifier, '["Input_185"]', text="End")
                        row.prop(ivy_modifier, '["Input_199"]', text="", icon ="ARROW_LEFTRIGHT")

                        col2 = box.column(align=True)
                        col2.label(text = "Align to Ground (-Z)")
                        row = col2.row(align = True)
                        row.prop(ivy_modifier, '["Input_184"]', text="Start")
                        row.prop(ivy_modifier, '["Input_182"]', text="End")
                        row.prop(ivy_modifier, '["Input_204"]', text="", icon ="ARROW_LEFTRIGHT")

                        col2 = box.column(align=True)
                        row = col2.row(align = True)
                        split = row.split(factor=0.6)
                        split.label(text = "Align to Target")
                        rowsp = split.row(align = True)
                        rowsp.prop(ivy_modifier, '["Input_205"]', invert_checkbox = True, text="Y")
                        rowsp.prop(ivy_modifier, '["Input_205"]', text="Z")
                        row = col2.row(align = True)
                        row.prop(ivy_modifier, '["Input_201"]', text="Start")
                        row.prop(ivy_modifier, '["Input_200"]', text="End")
                        row.prop(ivy_modifier, '["Input_203"]', text="", icon ="ARROW_LEFTRIGHT")
                        col2.prop(ivy_modifier, '["Input_202"]', text="Distance max")

                        col2 = box.column(align=True)
                        col2.label(text = "Rotation Local X")
                        row = col2.row(align = True)
                        row.prop(ivy_modifier, '["Input_157"]', text="Start")
                        row.prop(ivy_modifier, '["Input_156"]', text="End")
                        col2.prop(ivy_modifier, '["Input_158"]', text="Random")

                        col2 = box.column(align=True)
                        col2.label(text = "Rotation Local Y")
                        row = col2.row(align = True)
                        row.prop(ivy_modifier, '["Input_160"]', text="Start")
                        row.prop(ivy_modifier, '["Input_159"]', text="End")
                        col2.prop(ivy_modifier, '["Input_180"]', text="Random")

                        col2 = box.column(align=True)
                        col2.label(text = "Rotation Local Z")
                        row = col2.row(align = True)
                        row.prop(ivy_modifier, '["Input_163"]', text="Start")
                        row.prop(ivy_modifier, '["Input_162"]', text="End")
                        col2.prop(ivy_modifier, '["Input_164"]', text="Random")

                        col2 = box.column(align=True)
                        col2.label(text = "Scale")
                        row = col2.row(align = True)
                        row.prop(ivy_modifier, '["Input_166"]', text="Start")
                        row.prop(ivy_modifier, '["Input_165"]', text="End")
                        col2.prop(ivy_modifier, '["Input_167"]', text="Random")

                        box.prop(ivy_modifier, '["Input_193"]', text="Local Offset")
                        
                        box.prop(ivy_modifier, '["Input_187"]', text="Seed")
                        
                        col_two=box.column(align=True)
                        row = col_two.row(align=True)
                        row.scale_y = 1.8
                        add = row.operator("ivyadd.asset", text= "Add Flower", icon = 'ADD')
                        add.index = 21

                        row = col_two.row(align=True)
                        row.scale_y = 0.9
                        row.label(text="Source :")
                        row.prop(ivy_pref, 'panel_asset_source', text = "View 3D",  toggle = True)
                        row.prop(ivy_pref, 'panel_asset_source', text = "Asset Browser",  toggle = True, invert_checkbox=True)

                        col_two.separator(factor = 0.6)
                        row = col_two.row(align=True)
                        row.scale_y = 1.8
                        remove = row.operator("ivyremove.asset", text= "Remove Flower", icon = 'REMOVE')
                        remove.index = 21


                    # TRUNK
                    if ivy_pref.panel_sub_trunk == False:
                        col.separator(factor = 0.5)
                        col.prop(ivy_pref, 'panel_sub_trunk', text = "Branch Profile & Shader", emboss = False)
                        col.separator(factor = 1.5)
                    else:
                        box = col.box()
                        box.prop(ivy_pref, 'panel_sub_trunk', text = "Branch Profile & Shader", emboss = False)

                        row = box.row(align = True)
                        row.scale_y=1.4
                        row.operator('switch.buttonivy', depress = ivy_modifier["Input_133"], text = "Auto Radius").index = "Input_133"
                        tips = row.operator("bagaivy.tooltips", text="", emboss = True, depress = False, icon = 'INFO')
                        tips.message = "Branch radius will be adjusted based on the difference between the shortest and longest branches you draw. This adjustment is permanent and will occur each time you draw a new, longer or shorter curve. If you disable this feature, you will need to set the radius manually using Alt+S."
                        tips.title = "Auto Radius"
                        tips.image = "None"
                        tips.scale = 10
                        tips.url = "None"

                        col2 = box.column(align=True)
                        col2.prop(ivy_modifier, '["Input_135"]', text="Radius")
                        col2.prop(ivy_modifier, '["Input_134"]', text="Radius Repartition")
                        col2.prop(ivy_modifier, '["Input_136"]', text="Profil Resolution")
                        col2.operator('switch.buttonivy', depress = ivy_modifier["Input_172"], text = "Merge by Distance").index = "Input_172"
                        if ivy_modifier['Input_172']:
                            col2.prop(ivy_modifier, '["Input_173"]', text="Distance")

                        box.prop(ivy_modifier, '["Input_139"]', text="Twist")

                        col2 = box.column(align=True)
                        col2.label(text = "UV Scale")
                        row = col2.row(align = True)
                        row.prop(ivy_modifier, '["Input_137"]', text="X")
                        row.prop(ivy_modifier, '["Input_138"]', text="Y")

                        col2 = box.column(align=True)
                        col2.label(text = "Deform Branch Surface")
                        col2.prop(ivy_modifier, '["Input_140"]', text="Scale")
                        col2.prop(ivy_modifier, '["Input_141"]', text="Intensity")

                        box.prop(ivy_modifier, '["Input_187"]', text="Seed")

                        bark_mat = ivy_modifier['Input_48']
                        if bark_mat is not None:
                            if bark_mat.name.startswith('BIG_Ivy_Bark'):
                                
                                box.label(text="Material :")
                                row = box.row(align=True)
                                row.prop_search(ivy_modifier, '["Input_48"]', bpy.data, "materials", text="", icon="MATERIAL")


                                bark_node_group = bark_mat.node_tree.nodes['BIG_Ivy_Bark_Generator']
                                
                                col_mat = box.column(align=True)
                                col_mat.label(text="Mapping :")
                                col_mat.prop(bark_node_group.inputs[1], 'default_value', text = "Scale")
                                col_mat.prop(bark_node_group.inputs[2], 'default_value', text = "Stretching")

                                col_mat = box.column(align=True)
                                col_mat.label(text="Color :")
                                col_mat.prop(bark_node_group.inputs[3], 'default_value', text = "Luminosity")
                                col_mat.prop(bark_node_group.inputs[4], 'default_value', text = "Contrast")
                                col_mat.prop(bark_node_group.inputs[5], 'default_value', text = "Saturation")
                                col_mat.prop(bark_node_group.inputs[6], 'default_value', text = "Color Contrast")
                                col_mat.separator(factor = 0.3)
                                col_mat.prop(bark_node_group.inputs[8], 'default_value', text = "Tint Intensity")
                                col_mat.prop(bark_node_group.inputs[7], 'default_value', text = "")
                                
                                col_mat = box.column(align=True)
                                col_mat.prop(bark_node_group.inputs[9], 'default_value', text = "Specular")
                                col_mat.prop(bark_node_group.inputs[10], 'default_value', text = "Specular Tint")
                                col_mat.prop(bark_node_group.inputs[11], 'default_value', text = "Roughness")
                                col_mat.prop(bark_node_group.inputs[12], 'default_value', text = "Bump")
                                col_mat.prop(bark_node_group.inputs[13], 'default_value', text = "Displacement")
                            else:
                                box.label(text="Custom material detected.")
                                box.operator("wm.url_open", text="Setup UV Mapping", icon = 'PLAY', depress = False).url = "https://youtu.be/4Juv1lC2pt0"
                        
                        else:
                            box.label(text="Set material.")


                    # ANIMATION
                    if ivy_pref.panel_sub_animation == False:
                        col.separator(factor = 0.5)
                        col.prop(ivy_pref, 'panel_sub_animation', text = "Animation", emboss = False)
                        col.separator(factor = 1.5)
                    else:
                        box = col.box()
                        box.prop(ivy_pref, 'panel_sub_animation', text = "Animation", emboss = False)
                        box.label(text = "Method :")
                        row = box.row(align=True)
                        row.operator('switch.buttonivy', depress = not ivy_modifier["Input_65"], text = "Continue").index = "Input_65"
                        row.operator('switch.buttonivy', depress = ivy_modifier["Input_65"], text = "Loop").index = "Input_65"

                        tips = row.operator("bagaivy.tooltips", text="", depress = False, icon = 'INFO')
                        tips.message = 'The "Continue" method creates a fluctuating wind, which is not uniform. The "Loop" method is for animations made to loop (every X frames the animation will repeat without the transition being visible)..'
                        tips.title = "Animation Method"
                        tips.image = "None"
                        tips.scale = 10
                        tips.url = "https://youtu.be/CKUn79qzYWM"

                        if ivy_modifier["Input_65"] == True:
                            box.prop(ivy_modifier, '["Input_68"]', text = "Loop every X frames")
                            box.prop(ivy_modifier, '["Input_67"]', text = "Speed")
                        else:
                            box.prop(ivy_modifier, '["Input_66"]', text = "Turbility")
                            box.prop(ivy_modifier, '["Input_69"]', text = "Speed")
                        
                        col_hv = box.column(align = True)
                        col_hv.label(text = "Vertical :")
                        col_hv.prop(ivy_modifier, '["Input_70"]', text = "Influence Texture")
                        col_hv.prop(ivy_modifier, '["Input_71"]', text = "Time Offset")
                        col_hv.prop(ivy_modifier, '["Input_72"]', text = "Intensity")
                        col_hv.prop(ivy_modifier, '["Input_73"]', text = "Random Intensity")
                        
                        col_hv = box.column(align = True)
                        col_hv.label(text = "Horizontal :")
                        col_hv.prop(ivy_modifier, '["Input_74"]', text = "Influence Texture")
                        col_hv.prop(ivy_modifier, '["Input_75"]', text = "Time Offset")
                        col_hv.prop(ivy_modifier, '["Input_76"]', text = "Intensity")
                        col_hv.prop(ivy_modifier, '["Input_77"]', text = "Random Intensity")
                        col.separator(factor = 2.5)


                    # VISIBILITY
                    if ivy_pref.panel_sub_visibility == False:
                        col.separator(factor = 0.5)
                        col.prop(ivy_pref, 'panel_sub_visibility', text = "Visibility", emboss = False)
                        col.separator(factor = 1.5)
                    else:
                        box = col.box()
                        box.prop(ivy_pref, 'panel_sub_visibility', text = "Visibility", emboss = False)
                        
                        box.operator('switch.buttonivy', depress = not ivy_modifier["Input_26"], text = "Use leaf").index = "Input_26"
                        box.operator('switch.buttonivy', depress = ivy_modifier["Input_36"], text = "Use Flower").index = "Input_36"
                        row = box.row(align=True)
                        row.operator('switch.buttonivy', depress = ivy_modifier["Input_34"], text = "Use Proxy").index = "Input_34"
                        tips = row.operator("bagaivy.tooltips", text="", depress = False, icon = 'INFO')
                        tips.message = 'This option will create a low resolution of the ivy, only in the viewport. It will disapear in render.'
                        tips.title = "Orientation"
                        tips.image = "None"
                        tips.scale = 10
                        tips.url = "None"
                        box.operator('switch.buttonivy', depress = ivy_modifier["Input_40"], text = "Create Leaf Proxy").index = "Input_40"
                        col.separator(factor = 2.5)

                    # SOURCE OBJECTS
                    if ivy_pref.panel_sub_source_data == False:
                        col.separator(factor = 0.5)
                        col.prop(ivy_pref, 'panel_sub_source_data', text = "Source Objects", emboss = False)
                        col.separator(factor = 1.5)
                    else:
                        box = col.box()
                        box.prop(ivy_pref, 'panel_sub_source_data', text = "Source Objects", emboss = False)

                        box.label(text = "Targets :")
                        box.prop_search(ivy_modifier, '["Input_2"]', bpy.data, "collections", text="", icon="OUTLINER_COLLECTION")
                        box.label(text = "Start Points :")
                        box.prop_search(ivy_modifier, '["Input_3"]', bpy.data, "collections", text="", icon="OUTLINER_COLLECTION")
                        box.label(text = "Effectors :")                
                        box.prop_search(ivy_modifier, '["Input_56"]', bpy.data, "collections", text="", icon="OUTLINER_COLLECTION")


                        box.label(text = "Flowers Collection :")
                        row = box.row(align=True)
                        row.operator('switch.buttonivy', icon="OUTLINER_COLLECTION", depress = ivy_modifier["Input_19"], text = "").index = "Input_19"
                        row.operator('switch.buttonivy', icon = "OBJECT_DATA", depress = not ivy_modifier["Input_19"], text = "").index = "Input_19"
                        if ivy_modifier["Input_19"] == True:
                            row.prop_search(ivy_modifier, '["Input_21"]', bpy.data, "collections", text ="")
                        else:
                            row.prop_search(ivy_modifier, '["Input_20"]', bpy.data, "objects", text ="")


                        box.label(text = "Leaves Collection :")
                        row = box.row(align=True)
                        row.operator('switch.buttonivy', icon="OUTLINER_COLLECTION", depress = ivy_modifier["Input_22"], text = "").index = "Input_22"
                        row.operator('switch.buttonivy', icon = "OBJECT_DATA", depress = not ivy_modifier["Input_22"], text = "").index = "Input_22"
                        if ivy_modifier["Input_22"] == True:
                            row.prop_search(ivy_modifier, '["Input_24"]', bpy.data, "collections", text ="")
                        else:
                            row.prop_search(ivy_modifier, '["Input_23"]', bpy.data, "objects", text ="")

                        box.label(text = "Assets Rotation Offset:")
                        row = box.row(align=True)
                        row.prop(ivy_modifier, '["Input_43"]', text="")
                        tips = row.operator("bagaivy.tooltips", text="", depress = False, icon = 'INFO')
                        tips.message = 'Assets should be +Y oriented. If this is not the case, you can correct the rotation here.'
                        tips.title = "Orientation"
                        tips.image = "None"
                        tips.scale = 10
                        tips.url = "None"
                        col.separator(factor = 2.5)


                # END PANEL
                if bpy.context.object.mode == 'OBJECT':
                    row = col.row(align=True)
                    row.scale_y = 1.4
                    row.operator("ivy.draw", text= "Draw Mode", icon = 'OUTLINER_DATA_GP_LAYER')
                    row.operator("bagaivy.apply_ivy", text= "Apply Ivy", icon = 'CHECKMARK')
                    col_end=col.column(align=True)
                    col_end.alert = True
                    col_end.operator("ivy.delete", text= "Delete Selected Ivy", icon = 'TRASH')

                elif bpy.context.object.mode == 'EDIT':
                        row = col.row()
                        row.scale_y = 2
                        row.operator("ivy.draw", text= "EXIT", icon = 'LOOP_BACK')
                        if context.space_data.type == 'VIEW_3D':
                            tool = context.workspace.tools.from_space_view3d_mode(context.mode)
                            if ivy_modifier["Input_83"]:
                                col.operator("ivyedit.radius", text= "Edit Radius", depress = tool and tool.idname == "builtin.radius", icon ="GP_MULTIFRAME_EDITING")
                                col.operator("ivyedit.tilt", text= "Edit Tilt", depress = tool and tool.idname == "builtin.tilt", icon="FORCE_VORTEX")
                                col.operator("ivyedit.switchdirr", text= "Flip Branch Direction", icon="ARROW_LEFTRIGHT")
                            col.operator("ivyedit.draw", text= "Draw Ivy", depress = tool and tool.idname == "builtin.draw", icon="GREASEPENCIL")
        

        ###################################################################################
        # CREATE NEW IVY
        ###################################################################################  
        else:

            # MODES SELECTION
            col.label(text="Generaton mode :")
            main = col.row(align=True)
            main.scale_y = 2
            main.prop(ivy_pref, 'fast', text = "Fast",  toggle = True)
            main.prop(ivy_pref, 'accurate', text = "Accurate",  toggle = True)
            main.prop(ivy_pref, 'precision', text = "Precision",  toggle = True)

            # ABOUT IVY GENERATORS
            if ivy_pref.fast:
                if ivy_pref.panel_sub_about == False:
                    col.prop(ivy_pref, 'panel_sub_about', text = "About Fast mode", emboss = True, icon = "TRIA_RIGHT")
                    col.separator(factor = 1.5)
                else:
                    box = col.box()
                    box.prop(ivy_pref, 'panel_sub_about', text = "About Fast mode :", emboss = False, icon = "TRIA_DOWN")
                    col_about = box.column(align=True)
                    col_about.scale_y=0.8
                    text = "Generate ivy by drawing on your target's surface. The ivy produced is designed for quick computation at the expense of precision."
                    lines = split_text(text, 28)
                    for line in lines: col_about.label(text=line)
                    col_about.separator(factor = 1)
                    text = "This generator creates an initial 'piece' of ivy and replicates it around the drawn areas."
                    lines = split_text(text, 28)
                    for line in lines: col_about.label(text=line)
                    col_about.separator(factor = 1)
                    text = "We recommend using this ivy for backgrounds, large surfaces or in the secondary scene."
                    lines = split_text(text, 28)
                    for line in lines: col_about.label(text=line)

            elif ivy_pref.accurate:
                if ivy_pref.panel_sub_about == False:
                    col.prop(ivy_pref, 'panel_sub_about', text = "About Accurate mode", emboss = True, icon = "TRIA_RIGHT")
                    col.separator(factor = 1.5)
                else:
                    box = col.box()
                    box.prop(ivy_pref, 'panel_sub_about', text = "About Accurate mode :", emboss = False, icon = "TRIA_DOWN")
                    col_about = box.column(align=True)
                    col_about.scale_y=0.8
                    text = "Generates realistic ivy, including branch ramifications."
                    lines = split_text(text, 28)
                    for line in lines: col_about.label(text=line)
                    col_about.separator(factor = 1)
                    text = "This generator requires one or more 'Start Points' to determine the growth onset. By default, it uses the 3D Cursor's position for the first 'Start Point', but you can add as many as you wish. See 'Ivy Growth'."
                    lines = split_text(text, 28)
                    for line in lines: col_about.label(text=line)
                    col_about.separator(factor = 1)
                    text = "We recommend using this ivy for elements ranging from background to foreground."
                    lines = split_text(text, 28)
                    for line in lines: col_about.label(text=line)

            elif ivy_pref.precision:
                if ivy_pref.panel_sub_about == False:
                    col.prop(ivy_pref, 'panel_sub_about', text = "About Precision mode", emboss = True, icon = "TRIA_RIGHT")
                    col.separator(factor = 1.5)
                else:
                    box = col.box()
                    box.prop(ivy_pref, 'panel_sub_about', text = "About Precision mode :", emboss = False, icon = "TRIA_DOWN")
                    col_about = box.column(align=True)
                    col_about.scale_y=0.8
                    text = "Generate ivy branch by branch through drawing. You have the ability to manually adjust the radius and tilt of each branch."
                    lines = split_text(text, 28)
                    for line in lines: col_about.label(text=line)
                    col_about.separator(factor = 1)
                    text = "This generator is designed for manual editing and does not produce branch ramifications."
                    lines = split_text(text, 28)
                    for line in lines: col_about.label(text=line)
                    col_about.separator(factor = 1)
                    text = "We recommend using this for foreground elements, or whenever you require precision in the propagation and positioning of the ivy."
                    lines = split_text(text, 28)
                    for line in lines: col_about.label(text=line)

            
            # ASSETS SOURCE
            col.label(text="Assets Source :")
            row = col.row(align=True)
            row.scale_y = 0.9
            row.prop(ivy_pref, 'panel_asset_source', text = "View 3D",  toggle = True)
            row.prop(ivy_pref, 'panel_asset_source', text = "Asset Browser",  toggle = True, invert_checkbox=True)
            tips = row.operator("bagaivy.tooltips", text="", depress = False, icon = 'INFO')
            tips.message = "For 'View 3D' Asset Source, select assets, then an object for the ivy to grow on (only one target can be assigned initially in 'View 3D', but more can be added later). For 'Asset Browser' Source, multiple targets can be selected in 3D view, along with assets or a preset in the Asset Browser."
            tips.title = "About Assets source"
            tips.image = "None"
            tips.scale = 12
            tips.size = 50
            tips.url = "None"
            col.separator(factor = 1)
            
            # ADD IVY BUTTON
            if ivy_pref.panel_asset_source == False:
                area = find_areas('ASSETS')
                if obj is not None and obj.type == 'MESH':
                    if area is not None:
                        if area.ui_type == 'ASSETS':
                            row = col.row()
                            row.scale_y = 4
                            row.operator("bagaivy.add_ivy", text="Add New Ivy !", depress = False, icon = 'ADD')
                    else:
                        box = col.box()
                        box.scale_y = 3
                        box.label(text="Open the Asset Browser", icon = 'ASSET_MANAGER')
                    # col.label(text="Select ivy in Asset Browser")
                else:
                    box = col.box()
                    box.scale_y = 3
                    box.label(text="Select target (Mesh)", icon = 'BLANK1')
            else:
                if len(bpy.context.selected_objects) > 1:
                    row = col.row()
                    row.scale_y = 4
                    row.operator("bagaivy.add_ivy", text="Add New Ivy !", depress = False, icon = 'ADD')
                else:
                    box = col.box()
                    box.scale_y = 3
                    box.label(text="Select Assets, then Target")


            # HOW IT WORKS ?
            if ivy_pref.fast:
                tips = col.operator("bagaivy.tooltips", text="How it works ?", depress = False, icon = 'INFO')
                tips.message = "Select assets or preset to use and the surface for the ivy to grow on."
                tips.title = "How to add a new ivy :"
                tips.image = "None"
                tips.scale = 12
                tips.size = 50
                tips.url = "None"
            
            elif ivy_pref.accurate:
                if ivy_pref.panel_asset_source == False:
                    tips = col.operator("bagaivy.tooltips", text="How it works ?", depress = False, icon = 'INFO')
                    tips.message = '(1) First select your targets (objects). (2) Then set a start point by positionning the 3D Cursor (ivy will grow from this point). (3) Open the Asset browser and select your leaves (one or multiple objects). (4) Use "Add New Ivy" and draw !'
                    tips.title = "How to add a new ivy :"
                    tips.image = "first_step"
                    tips.scale = 12
                    tips.size = 50
                    tips.url = "https://youtu.be/l28asatUXBw"
                else:
                    tips = col.operator("bagaivy.tooltips", text="How it works ?", depress = False, icon = 'INFO')
                    tips.message = '(1) First select your assets. (2) Then add your target to the selection. (3) Set a start point by positionning the 3D Cursor (ivy will grow from this point). (4) Use "Add New Ivy" and draw !'
                    tips.title = "How to add a new ivy :"
                    tips.image = "first_step"
                    tips.scale = 12
                    tips.size = 50
                    tips.url = "https://youtu.be/l28asatUXBw"

            elif ivy_pref.precision:
                tips = col.operator("bagaivy.tooltips", text="How it works ?", depress = False, icon = 'INFO')
                tips.message = "Select assets or preset to use and the surface for the ivy to grow on."
                tips.title = "How to add a new ivy :"
                tips.image = "None"
                tips.scale = 12
                tips.size = 50
                tips.url = "None"


class Switch1Operator(Operator):
    bl_idname = "bagaivy.switch_1"
    bl_label = "Switch 1"

    def execute(self, context):
        obj = context.object
        ivy_modifier = obj.modifiers["Baga_Ivy_Generator_V2"]
        ivy_modifier["Input_81"] = True
        ivy_modifier["Input_82"] = False
        ivy_modifier["Input_83"] = False

        # UPDATE UVs LINKS
        node_group = ivy_modifier.node_group
        node_from = node_group.nodes.get('bagaivy_generator_fast_uvs')
        node_to = node_group.nodes.get('bagaivy_generator_uvs')
        if node_from is not None and node_to is not None:
            socket_out = node_from.outputs[0]
            socket_in = node_to.inputs[0]
            node_group.links.new(socket_out, socket_in)

        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
        bpy.ops.bagaivy.tooltips('INVOKE_DEFAULT', message='Please be aware that the Fast, Accurate, and Precision generation modes are distinct and designed for different purposes. The resulting ivy will vary significantly from one mode to another. Also, note that changes made to the settings/values in one mode may not be synchronized across the others.', title="Warning : Ivy Modes", image="None", scale=10, url="None")
        return {'FINISHED'}

class Switch2Operator(Operator):
    bl_idname = "bagaivy.switch_2"
    bl_label = "Switch 2"

    def execute(self, context):
        obj = context.object
        ivy_modifier = obj.modifiers["Baga_Ivy_Generator_V2"]
        ivy_modifier["Input_81"] = False
        ivy_modifier["Input_82"] = True
        ivy_modifier["Input_83"] = False

        # UPDATE UVs LINKS
        node_group = ivy_modifier.node_group
        node_from = node_group.nodes.get('bagaivy_generator_accurate_uvs')
        node_to = node_group.nodes.get('bagaivy_generator_uvs')
        if node_from is not None and node_to is not None:
            socket_out = node_from.outputs[0]
            socket_in = node_to.inputs[0]
            node_group.links.new(socket_out, socket_in)

        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
        bpy.ops.bagaivy.tooltips('INVOKE_DEFAULT', message='Please be aware that the Fast, Accurate, and Precision generation modes are distinct and designed for different purposes. The resulting ivy will vary significantly from one mode to another. Also, note that changes made to the settings/values in one mode may not be synchronized across the others.', title="Warning : Ivy Modes", image="None", scale=10, url="None")
        return {'FINISHED'}

class Switch3Operator(Operator):
    bl_idname = "bagaivy.switch_3"
    bl_label = "Switch 3"

    def execute(self, context):
        obj = context.object
        ivy_modifier = obj.modifiers["Baga_Ivy_Generator_V2"]
        ivy_modifier["Input_81"] = False
        ivy_modifier["Input_82"] = False
        ivy_modifier["Input_83"] = True

        # UPDATE UVs LINKS
        node_group = ivy_modifier.node_group
        node_from = node_group.nodes.get('bagaivy_generator_precision_uvs')
        node_to = node_group.nodes.get('bagaivy_generator_uvs')
        if node_from is not None and node_to is not None:
            socket_out = node_from.outputs[0]
            socket_in = node_to.inputs[0]
            node_group.links.new(socket_out, socket_in)

        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
        bpy.ops.bagaivy.tooltips('INVOKE_DEFAULT', message='Please be aware that the Fast, Accurate, and Precision generation modes are distinct and designed for different purposes. The resulting ivy will vary significantly from one mode to another. Also, note that changes made to the settings/values in one mode may not be synchronized across the others.', title="Warning : Ivy Modes", image="None", scale=10, url="None")
        return {'FINISHED'}
    
def split_text(text, max_line_length):
    words = text.split(' ')
    lines = []
    current_line = ''

    for word in words:
        if len(current_line) + len(word) > max_line_length:
            lines.append(current_line.strip())
            current_line = word
        else:
            current_line += ' ' + word

    lines.append(current_line.strip())  # Don't forget the last line
    return lines

###################################################################################
# UI SWITCH BUTON
###################################################################################
class IVY_OP_switchinput(bpy.types.Operator):
    bl_idname = "switch.buttonivy"
    bl_label = "switch.buttonivy"

    index: bpy.props.StringProperty(name="None")
    def execute(self, context):

        obj = context.object
        try:
            modifier = obj.modifiers["Baga_Ivy_Generator_V2"]
        except KeyError:
            modifier = obj.modifiers["Baga_Ivy_Generator"]
        blender_version = bpy.app.version
        minimum_version = (3, 5, 0)
        if blender_version >= minimum_version:
            if modifier[self.index] == True:
                modifier[self.index] = False
            else:
                modifier[self.index] = True
        else:
            if modifier[self.index] == 1:
                modifier[self.index] = 0
            else:
                modifier[self.index] = 1
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}


###################################################################################
# SET IVY RADIUS (Precision mode)
###################################################################################
class IVY_OP_editivy_radius(bpy.types.Operator):
    """Set branch radius, will also influence leaves/fruits count and radius. ONLY in Precision mode. Shortcut : Alt S"""
    bl_idname = "ivyedit.radius"
    bl_label = "Edit Radius"
    def execute(self, context):
        bpy.ops.wm.tool_set_by_id(name="builtin.radius")
        return {'FINISHED'}
    
    
###################################################################################
# DRAW IVY
###################################################################################
class IVY_OP_editivy_draw(bpy.types.Operator):
    """Enable pen for ivy draw on surface"""
    bl_idname = "ivyedit.draw"
    bl_label = "Draw Ivy"
    def execute(self, context):
        bpy.ops.wm.tool_set_by_id(name="builtin.draw")
        bpy.context.scene.tool_settings.curve_paint_settings.depth_mode = 'SURFACE'
        return {'FINISHED'}
    
    
###################################################################################
# SET IVY Tilt
###################################################################################
class IVY_OP_editivy_tilt(bpy.types.Operator):
    """Set branch tilt. ONLY in Precision mode. Shortcut : Ctrl T"""
    bl_idname = "ivyedit.tilt"
    bl_label = "Adit Tilt Ivy"
    def execute(self, context):
        bpy.ops.wm.tool_set_by_id(name="builtin.tilt")
        return {'FINISHED'}
    
    
###################################################################################
# INVERT CURVE DIRECTION
###################################################################################
class IVY_OP_editivy_switchdirr(bpy.types.Operator):
    """Invert curve direction"""
    bl_idname = "ivyedit.switchdirr"
    bl_label = "Adit Tilt Ivy"
    def execute(self, context):
        bpy.ops.curve.switch_direction()
        return {'FINISHED'}
    

###################################################################################
# FIND AREAS
###################################################################################
def find_areas(type):
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
# DISPLAY WARNING
###################################################################################
def Warning(message = "", title = "Message Box", icon = 'INFO'):

    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)


###################################################################################
# DISPLAY TOOLTIPS
###################################################################################
class IVY_tooltips(Operator):
    """Display a tooltips"""
    bl_idname = "bagaivy.tooltips"
    bl_label = "Tips"

    message: bpy.props.StringProperty(default="None")
    title: bpy.props.StringProperty(default="Tooltip")
    icon: bpy.props.StringProperty(default="INFO")
    image: bpy.props.StringProperty(default="None")
    scale: bpy.props.FloatProperty(default=5)
    size: bpy.props.IntProperty(default=50)
    url: bpy.props.StringProperty(default="None")

    def execute(self, context):
        Tooltip(self.message, self.title, self.icon, self.image, self.scale, self.size, self.url) 
        return {'FINISHED'}

def Tooltip(message = "", title = "Message Box", icon = 'INFO', image = "None", scale = 5, size = 50, url = "None"):

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        if image != "None":
            col.template_icon(icon_value = icons.previews[image].icon_id, scale=scale)
        # DIRTY LAZY CODE START
        count = 0
        mess = message
        length = int(size)
        caracter = length
        temp = 0
        for i in message:            
            if count == 0:
                if mess[0] == " ":
                    o = length
                    if len(mess) > o:
                        while mess[o] != " ":
                            o += 1
                            if len(mess) == o:
                                break
                    col.label(text=mess[1:o])
                    caracter = length

                elif mess == message:
                    o = length
                    if o >= len(mess):
                        o = len(mess)-1
                    while message[o] != " ":
                        o += 1
                        if len(mess) == o:
                            break
                    col.label(text=mess[0:o])
                    caracter = length                    
                else :
                    count = temp
                    caracter += 1
            count += 1
            temp = count
            mess = mess[1:]
            if count == caracter:
                count = 0
        # DIRTY LAZY CODE END
        if url != "None":
            col.separator(factor = 1.5)
            col.operator("wm.url_open", text="Video Demo", icon = 'PLAY', depress = False).url = url


    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)


###################################################################################
# ADD ASSETS
###################################################################################
class IVY_ADD_Assets(Operator):
    """Add asset to the selected ivy"""
    bl_idname = "ivyadd.asset"
    bl_label = "Add Asset"
    bl_options = {'REGISTER', 'UNDO'}

    index: bpy.props.IntProperty(name="Input Index", default=0)

    @classmethod
    def poll(cls, context):
        return (bpy.context.object.mode == 'OBJECT')

    def execute(self, context):
        
        target = bpy.context.active_object
        try:
            ivy_modifier = target.modifiers["Baga_Ivy_Generator_V2"]
        except KeyError:
            ivy_modifier = target.modifiers["Baga_Ivy_Generator"]
        collection = ivy_modifier["Input_"+str(self.index)]
        ivy_pref = context.preferences.addons['BagaIvy'].preferences
        
        # FROM ASSET BROWSER
        if ivy_pref.panel_asset_source == False:
            area = find_areas('ASSETS')
            if area is not None:
                if area.ui_type == 'ASSETS':

                    win = find_window('ASSETS')

                    #current_library_name = area.spaces.active.params.asset_library_ref old one
                    current_library_name = area.spaces.active.params.asset_library_reference
                    if current_library_name == "LOCAL":
                        library_path = Path(bpy.data.filepath)
                    else:
                        library_path = Path(context.preferences.filepaths.asset_libraries.get(current_library_name).path)

                    with context.temp_override(window=win, area = area):
                        print("Imported Assets :")
                        for asset_file in context.selected_assets:
                            print(asset_file.full_library_path)
                            print(asset_file.full_path)
                            asset_fullpath = asset_file.full_path
                            if current_library_name == "LOCAL":
                                asset_fullpath /= asset_file.local_id.name

                            asset_filepath = asset_file.full_library_path
                            inner_path = ntpath.basename(ntpath.dirname(asset_fullpath))
                            asset_name = ntpath.basename(asset_fullpath)
                            print(asset_name)
                            time.sleep(1)

                            try:
                                bpy.ops.object.select_all(action='DESELECT')
                                bpy.data.objects[asset_name].select_set(True)
                                asset = bpy.context.selected_objects
                            except:
                                bpy.ops.wm.append(
                                    filepath=os.path.join(asset_filepath, inner_path, asset_name),
                                    directory=os.path.join(asset_filepath, inner_path),
                                    filename=asset_name
                                    )
                                asset = bpy.context.selected_objects

                                for a in asset:
                                    for col in a.users_collection:
                                        col.objects.unlink(a)
                            for a in asset:
                                if a.name not in collection.objects:
                                    collection.objects.link(a)
                    
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.context.view_layer.objects.active = target
                    target.select_set(True)

                else: 
                    Warning(message = "Open and select assets in the asset browser.", title = "Wrong selection", icon = 'INFO')
                    return {'FINISHED'}
            else: 
                Warning(message = "Open and select assets in the asset browser.", title = "Wrong selection", icon = 'INFO')
                return {'FINISHED'}


        # FROM VIEW 3D
        else:
            assets = bpy.context.selected_objects
            if target in assets:
                assets.remove(target)

            if len(assets) < 1:
                Warning(message = "First select assets you want to add. Then add ivy to selection before using : + Add Assets.", title = "Wrong selection", icon = 'INFO')
                return {'FINISHED'}

            for asset in assets:
                if asset.name not in collection.objects:
                    collection.objects.link(asset)
        
        return {'FINISHED'}


###################################################################################
# REMOVE ASSETS
###################################################################################
class IVY_REMOVE_Assets(Operator):
    """Remove asset to the selected ivy"""
    bl_idname = "ivyremove.asset"
    bl_label = "Remove Asset"
    bl_options = {'REGISTER', 'UNDO'}

    index: bpy.props.IntProperty(name="Input Index", default=0)

    @classmethod
    def poll(cls, context):
        return (bpy.context.object.mode == 'OBJECT')

    def execute(self, context):
        
        target = bpy.context.active_object
        try:
            ivy_modifier = target.modifiers["Baga_Ivy_Generator_V2"]
        except KeyError:
            ivy_modifier = target.modifiers["Baga_Ivy_Generator"]
        collection = ivy_modifier["Input_"+str(self.index)]
        assets = bpy.context.selected_objects
        if target in assets:
            assets.remove(target)

        if len(assets) < 1:
            Warning(message = "First select assets you want to remove. Then add ivy to selection before using : + Remove Assets.", title = "Wrong selection", icon = 'INFO')
            return {'FINISHED'}

        for asset in assets:
            if asset.name in collection.objects:
                collection.objects.unlink(asset)
        
        return {'FINISHED'}
   

###################################################################################
# ADD START POINT
###################################################################################
class IVY_Add_Start_Point(Operator):
    """Add a new start point for the selected ivy"""
    bl_idname = "ivyadd.startpoint"
    bl_label = "Add Start Point"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        target = bpy.context.active_object
        try:
            ivy_modifier = target.modifiers["Baga_Ivy_Generator_V2"]
        except KeyError:
            ivy_modifier = target.modifiers["Baga_Ivy_Generator"]
        collection = ivy_modifier["Input_3"]
        assets = bpy.context.selected_objects

        ###################################################################################
        # SET START POINT
        ###################################################################################
        bpy.ops.mesh.primitive_ico_sphere_add(radius = 0.1, location=bpy.context.scene.cursor.location)
        start_point = bpy.context.selected_objects
        for s in start_point:
            for col in s.users_collection:
                col.objects.unlink(s)
            collection.objects.link(s)
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

        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = target
        for ob in assets:
            ob.select_set(True)
        target.select_set(True)

        return {'FINISHED'}

        
###################################################################################
# EDIT MODE
###################################################################################
class IVY_Draw_New(Operator):
    """Switch to draw mode for ivy"""
    bl_idname = "ivy.draw"
    bl_label = "Draw mode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.editmode_toggle()
        if bpy.context.object.mode == 'EDIT':
            bpy.context.scene.tool_settings.curve_paint_settings.depth_mode = 'SURFACE'
            bpy.ops.wm.tool_set_by_id(name="builtin.draw")
        return {'FINISHED'}

        
###################################################################################
# ADD TARGET
###################################################################################
class IVY_ADD_Target(Operator):
    """Adds the selected object as a target for the ivy to grow on. Select your object then the ivy."""
    bl_idname = "ivyadd.target"
    bl_label = "Add Asset"
    bl_options = {'REGISTER', 'UNDO'}

    index: bpy.props.IntProperty(name="Input Index", default=0)

    @classmethod
    def poll(cls, context):
        return (bpy.context.object.mode == 'OBJECT')

    def execute(self, context):
        
        target = bpy.context.active_object
        try:
            ivy_modifier = target.modifiers["Baga_Ivy_Generator_V2"]
        except KeyError:
            ivy_modifier = target.modifiers["Baga_Ivy_Generator"]
        collection = ivy_modifier["Input_"+str(self.index)]

        assets = bpy.context.selected_objects
        if target in assets:
            assets.remove(target)

        if len(assets) < 1:
            Warning(message = "First select assets you want to add. Then add ivy to selection before using : + Add Assets.", title = "Wrong selection", icon = 'INFO')
            return {'FINISHED'}

        for asset in assets:
            if asset.name not in collection.objects:
                collection.objects.link(asset)
        
        return {'FINISHED'}


###################################################################################
# REMOVE TARGET
###################################################################################
class IVY_REMOVE_Target(Operator):
    """Remove the selected object from the target collection. Select your object then the ivy."""
    bl_idname = "ivyremove.target"
    bl_label = "Remove Asset"
    bl_options = {'REGISTER', 'UNDO'}

    index: bpy.props.IntProperty(name="Input Index", default=0)

    @classmethod
    def poll(cls, context):
        return (bpy.context.object.mode == 'OBJECT')

    def execute(self, context):
        
        target = bpy.context.active_object
        try:
            ivy_modifier = target.modifiers["Baga_Ivy_Generator_V2"]
        except KeyError:
            ivy_modifier = target.modifiers["Baga_Ivy_Generator"]
        collection = ivy_modifier["Input_"+str(self.index)]
        assets = bpy.context.selected_objects
        if target in assets:
            assets.remove(target)

        if len(assets) < 1:
            Warning(message = "First select assets you want to remove. Then add ivy to selection before using : + Remove Assets.", title = "Wrong selection", icon = 'INFO')
            return {'FINISHED'}

        for asset in assets:
            if asset.name in collection.objects:
                collection.objects.unlink(asset)
        
        return {'FINISHED'}
   
