# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# Branch : Blender 4.0

bl_info = {
    "name" : "Baga Ivy Generator",
    "author" : "Antoine Bagattini, Laura Mercadal, Theo Chevret",
    "description" : "",
    "blender" : (4, 0, 0),
    "version" : (2, 0, 2),
    "location" : "View3D > Sidebar > BagaIvy",
    "warning" : "",
    "category" : "Generic"
}

from re import T
import bpy

from . ivy_ui import (
    IVY_PT_Panel, 
    IVY_OP_switchinput, 
    IVY_tooltips, 
    IVY_ADD_Assets, 
    IVY_REMOVE_Assets, 
    IVY_Add_Start_Point,
    IVY_Draw_New,
    IVY_ADD_Target,
    IVY_REMOVE_Target,
    Switch1Operator,
    Switch2Operator,
    Switch3Operator,
    IVY_OP_editivy_radius,
    IVY_OP_editivy_draw,
    IVY_OP_editivy_tilt,
    IVY_OP_editivy_switchdirr,
    )
from . ivy_add import IVY_OP_add
from . Ivy_asset_browser import IVY_OP_SetupAssetBrowser
from . Ivy_delete import IVY_DELETE_Ivy
from . ivy_apply import IVY_OP_apply
from . ivy_replace import IVY_REPLACE_Ivy
from . import icons



#############
# PREFERENCES
#############
def update_fast(self, context):
    if self.fast:
        self.accurate = False
        self.precision = False

def update_accurate(self, context):
    if self.accurate:
        self.fast = False
        self.precision = False

def update_precision(self, context):
    if self.precision:
        self.fast = False
        self.accurate = False

class IVY_Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    
    # default generator
    fast: bpy.props.BoolProperty(name="Fast", default=False, update=update_fast)
    accurate: bpy.props.BoolProperty(name="Accurate", default=True, update=update_accurate)
    precision: bpy.props.BoolProperty(name="Precision", default=False, update=update_precision)
    
    panel_sub_method: bpy.props.BoolProperty(name="Computing Methods", default=False)
    panel_sub_about: bpy.props.BoolProperty(name="About", default=False)
    panel_sub_distribution: bpy.props.BoolProperty(name="Distribution", default=False)
    panel_sub_distribution_avanced: bpy.props.BoolProperty(name="Distribution", default=False)
    panel_sub_island: bpy.props.BoolProperty(name="Island", default=False)
    panel_sub_leaf: bpy.props.BoolProperty(name="Leaf", default=False)
    panel_sub_flower: bpy.props.BoolProperty(name="Leaf", default=False)
    panel_sub_leaf_avanced: bpy.props.BoolProperty(name="Leaf", default=False)
    panel_sub_flower_avanced: bpy.props.BoolProperty(name="Leaf", default=False)
    panel_sub_source_data: bpy.props.BoolProperty(name="Source Data", default=False)
    panel_sub_visibility: bpy.props.BoolProperty(name="Source Data", default=False)
    panel_sub_tools: bpy.props.BoolProperty(name="Source Data", default=False)
    panel_sub_trunk: bpy.props.BoolProperty(name="Trunk", default=False)
    panel_sub_effector: bpy.props.BoolProperty(name="Effector", default=False)
    panel_sub_animation: bpy.props.BoolProperty(name="Animation", default=False)

    panel_asset_source: bpy.props.BoolProperty(name="Source Data", default=False)

    assets_path: bpy.props.StringProperty(name="Database Location", default="Paste Bagapie's new Blender files location here.")
    use_custom_location: bpy.props.BoolProperty(name="Database Location", default=False)

    
    asset_browser: bpy.props.BoolProperty(name="Asset Browser Preferences", default=False)
    support: bpy.props.BoolProperty(name="Support Preferences", default=False)
    our_addon: bpy.props.BoolProperty(name="Support Preferences", default=False)


    def draw(self, context):
        layout = self.layout
        

        ###################################################################################
        # ASSET BROWSER
        ###################################################################################
        box = layout.box()
        box.prop(self, 'asset_browser', text = "Asset Browser", emboss = False, icon = "ASSET_MANAGER")
        if self.asset_browser == True:
            col = box.column(align=True)
            col.scale_y = 2
            col.operator('bagaivy.ivyassetslibrary', icon = "ASSET_MANAGER")


        box = layout.box()
        box.prop(self, 'support', text = "Support & Documentation", emboss = False, icon = "ASSET_MANAGER")
        if self.support == True:
            box.label(text = "This addon need BagaPie Modifier.")  

            row = box.row(align=True)
            row.scale_y = 1.5
            row.operator("wm.url_open", text="Documentation", icon = 'TEXT').url = "https://www.f12studio.fr/ivy-generator"
            row.operator("wm.url_open", text="Help !", icon = 'VIEW_PAN').url = "https://discord.gg/b7wg9rSKc7"
            row.operator("wm.url_open", text="Support & bug report", icon = 'MODIFIER').url = "https://discord.gg/b7wg9rSKc7"
            row = box.row(align=True)
            row.scale_y = 1.5
            row.operator("wm.url_open", text="BagaPie BlenderArtists Topic", icon = 'COMMUNITY').url = "https://blenderartists.org/t/baga-ivy-generator-addon/1418418"
            row.operator("wm.url_open", text="BagaPie Discord", icon = 'COMMUNITY').url = "https://discord.gg/b7wg9rSKc7"
            row = box.row(align=True)
            row.scale_y = 1.5
            row.operator("wm.url_open", text="Video Demo", icon = 'PLAY').url = "https://youtu.be/l28asatUXBw"


        ###################################################################################
        # OUR ADDONS
        ###################################################################################
        box = layout.box()
        box.prop(self, 'our_addon', text = "Our Addons !", emboss = False, icon = "FUND")
        if self.our_addon == True:
            col = box.column(align=True)
            row = col.row(align=True)
            row.scale_y = 1.5
            row.operator("wm.url_open", text="BagaPie Assets", icon = 'FUND').url = "https://abaga.gumroad.com/l/GcYmPC"
            row.scale_x = 2
            row.operator("wm.url_open", text="", icon = 'PLAY').url = "https://youtu.be/tRIDwMEugns"
            row = box.row(align=True)
            row.scale_y = 1.5
            row.operator("wm.url_open", text="Quick Compo", icon = 'FUND').url = "https://abaga.gumroad.com/l/QCompo"
            row.scale_x = 2
            row.operator("wm.url_open", text="", icon = 'PLAY').url = "https://youtu.be/ZGN9YxvqXgM"

            col = box.column(align=True)
            col.label(text="Generators / Little Addons / Files :")
            row = col.row(align=True)
            row.scale_x = 1.2
            row.operator("wm.url_open", text="Symbiote Generator").url = "https://abaga.gumroad.com/l/SkyIVq"
            row.operator("wm.url_open", text="Rain Generator").url = "https://abaga.gumroad.com/l/rain"
            row.operator("wm.url_open", text="Blender and Print SpongeBob").url = "https://laura3dcraft.gumroad.com/l/bcvfa"
            row = col.row(align=True)
            row.scale_x = 1.2
            row.operator("wm.url_open", text="Ivy Generator").url = "https://abaga.gumroad.com/l/ivygen"
            row.operator("wm.url_open", text="Arch Generator").url = "https://abaga.gumroad.com/l/UlIvj"
            row.operator("wm.url_open", text="BagaPassesSaver").url = "https://abaga.gumroad.com/l/MQcAd"
            row = col.row(align=True)
            row.scale_x = 1.2
            row.operator("wm.url_open", text="Render Device Switcher").url = "https://abaga.gumroad.com/l/AKNdXX"
            row.operator("wm.url_open", text="Lego Generator").url = "https://abaga.gumroad.com/l/zlcrs"
            row.operator("wm.url_open", text="Fantasy Gate Generator").url = "https://abaga.gumroad.com/l/hcvvq"


classes = [
    IVY_PT_Panel,
    IVY_OP_add,
    IVY_OP_switchinput,
    IVY_tooltips,
    IVY_Preferences,
    IVY_ADD_Assets,
    IVY_REMOVE_Assets,
    IVY_Add_Start_Point,
    IVY_Draw_New,
    IVY_OP_SetupAssetBrowser,
    IVY_ADD_Target,
    IVY_REMOVE_Target,
    IVY_DELETE_Ivy,
    IVY_OP_apply,
    Switch1Operator,
    Switch2Operator,
    Switch3Operator,
    IVY_OP_editivy_radius,
    IVY_OP_editivy_draw,
    IVY_OP_editivy_tilt,
    IVY_OP_editivy_switchdirr,
    IVY_REPLACE_Ivy,
    ]

def register():
    icons.import_icons()
    
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    icons.unload_icons()
    
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()