import bpy
from bpy.types import Operator

class IVY_OP_apply(Operator):
    """ Apply ivy """
    bl_idname = "bagaivy.apply_ivy"
    bl_label = 'Add Ivy'
    bl_options = {'REGISTER', 'UNDO'}

    instances_count: bpy.props.IntProperty(default=0)
    instances_polygon_count: bpy.props.IntProperty(default=0)
    delete_assets_coll: bpy.props.BoolProperty(default=True)

    @classmethod
    def poll(cls, context):
        return (bpy.context.object.mode == 'OBJECT')

    def invoke(self, context, event):
        wm = context.window_manager
        
        return wm.invoke_props_dialog(self)


    def draw(self, context):
        obj = context.object
        try:
            ivy_modifier = obj.modifiers["Baga_Ivy_Generator_V2"]
        except KeyError:
            ivy_modifier = obj.modifiers["Baga_Ivy_Generator"]
        self.instances_polygon_count = 0
        self.instances_count = 0

        depsgraph = bpy.context.evaluated_depsgraph_get()
        eval = obj.evaluated_get(depsgraph)
        instA = [inst for inst in depsgraph.object_instances if inst.is_instance and inst.parent == eval]

        coll_assets=[]
        assets_count =0

        # LEAF
        if ivy_modifier['Input_22'] == True:
            try:
                coll_assets.append(ivy_modifier['Input_24'])
                assets_count += len(ivy_modifier['Input_24'].objects)
            except: pass
        else:
            try:
                self.instances_polygon_count += len(ivy_modifier['Input_23'].data.polygons)
                assets_count += 1
            except: pass
        # FLOWER
        if ivy_modifier['Input_19'] == True:
            try:
                coll_assets.append(ivy_modifier['Input_21'])
                assets_count += len(ivy_modifier['Input_21'].objects)
            except: pass
        else:
            try:
                self.instances_polygon_count += len(ivy_modifier['Input_20'].data.polygons)
                assets_count += 1
            except: pass

        for coll in coll_assets:
            for ob in coll.objects:
                self.instances_polygon_count += len(ob.data.polygons)

        self.instances_count = int(len(instA)*(self.instances_polygon_count/assets_count))

        layout = self.layout
        col = layout.column(align=True)
        col.label(text = "{} instances detected (leaves and flowers).".format(str(len(instA))))
        col.label(text = "About {} polygons will be created.".format(str(self.instances_count)))
        col.separator(factor = 1.5)
        col.label(text = "This convertion may break your UVs !")
        col.label(text = "If custom assets are used, please name these UVs: UVMap")
        if self.delete_assets_coll == True:
            col.prop(self, 'delete_assets_coll', text = "Keep leaves and flowers (assets) in this scene", emboss = True, invert_checkbox = not self.delete_assets_coll, icon = 'OUTLINER_COLLECTION')
        else:
            col.prop(self, 'delete_assets_coll', text = "Keep leaves and flowers (assets) in this scene", emboss = True, invert_checkbox = self.delete_assets_coll, icon = 'OUTLINER_COLLECTION')
        # print(self.delete_assets_coll)
        col.label(text = "Continue ?")

    def execute(self, context):

        obj = context.object
        try:
            modifier = obj.modifiers["Baga_Ivy_Generator_V2"]
        except KeyError:
            modifier = obj.modifiers["Baga_Ivy_Generator"]
        modifier['Input_52'] = 1 if bpy.app.version < (3, 5, 0) else True
            
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)

        bpy.ops.object.convert(target='MESH')

        objects_coll = []

        ivy_colls = obj.users_collection
        for coll in ivy_colls:
            if coll.name.startswith('BIG_Ivy'):
                for parent_collection in bpy.data.collections:
                    if coll.name in parent_collection.children.keys():
                        if parent_collection.name.startswith('BIG_Ivy Generated'):
                            main_coll = parent_collection
                            for colls in parent_collection.children.keys():
                                if colls.startswith('BIG_Targets'):
                                    target_coll = bpy.data.collections[colls]
                                elif colls.startswith('BIG_Ivy_Assets'):
                                    assets_coll = bpy.data.collections[colls]
                                    if self.delete_assets_coll == False:
                                        objects_coll.append(assets_coll)
                                elif colls.startswith('BIG_Ivy_Start_Point'):
                                    start_point_coll = bpy.data.collections[colls]
                                    objects_coll.append(start_point_coll)
                                elif colls.startswith('BIG_Effector'):
                                    start_effector = bpy.data.collections[colls]
                                elif colls.startswith('BIG_Ivy_Flowers'):
                                    flower_coll = bpy.data.collections[colls]
                                    if self.delete_assets_coll == False:
                                        objects_coll.append(flower_coll)
        
        for col in objects_coll:
            for o in col.all_objects:
                if len(o.users_collection) > 1:
                    col.objects.unlink(o) 
                else:
                    bpy.data.objects.remove(o, do_unlink=True)
            bpy.data.collections.remove(col)

        for o in start_effector.all_objects:
            start_effector.objects.unlink(o) 
        bpy.data.collections.remove(start_effector)

        for o in target_coll.all_objects:
            target_coll.objects.unlink(o) 
        bpy.data.collections.remove(target_coll)
        # bpy.data.collections.remove(main_coll)
        
        if bpy.app.version < (3, 5, 0):
            obj.data.attributes.active_index = 0
            for at in obj.data.attributes:
                if at.name == "UVMap":
                    bpy.ops.geometry.attribute_convert(mode="UV_MAP")
                else:
                    obj.data.attributes.active_index += 1

            obj.data.attributes.active_index = 0
            for at in obj.data.attributes:
                if at.name == "UVs":
                    bpy.ops.geometry.attribute_convert(mode="UV_MAP")
                else:
                    obj.data.attributes.active_index += 1

        obj.name = obj.name + "_Bake"
        
        return {'FINISHED'}