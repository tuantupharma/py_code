import bpy
import time
        
        
class IVY_DELETE_Ivy(bpy.types.Operator):
    """Delete selected ivy"""
    bl_idname = "ivy.delete"
    bl_label = "Delete Ivy"
    bl_options = {'REGISTER', 'UNDO'}
    
    keep_assets_coll: bpy.props.BoolProperty(default=True)

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        if self.keep_assets_coll == True:
            col.prop(self, 'keep_assets_coll', text = "Keep assets used by this ivy in this scene.", emboss = True, invert_checkbox = not self.keep_assets_coll, icon = 'OUTLINER_COLLECTION')
        else:
            col.prop(self, 'keep_assets_coll', text = "Keep assets used by this ivy in this scene.", emboss = True, invert_checkbox = self.keep_assets_coll, icon = 'OUTLINER_COLLECTION')


    def execute(self, context):
        target = bpy.context.active_object
        objects_coll = []

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
                                    if self.keep_assets_coll == False:
                                        objects_coll.append(assets_coll)
                                elif colls.startswith('BIG_Ivy_Start_Point'):
                                    start_point_coll = bpy.data.collections[colls]
                                    objects_coll.append(start_point_coll)
                                elif colls.startswith('BIG_Effector'):
                                    start_effector = bpy.data.collections[colls]
                                elif colls.startswith('BIG_Ivy_Flowers'):
                                    flower_coll = bpy.data.collections[colls]
                                    if self.keep_assets_coll == False:
                                        objects_coll.append(flower_coll)
                            objects_coll.append(ivy_coll)
        

        for o in start_effector.all_objects:
            start_effector.objects.unlink(o) 
        bpy.data.collections.remove(start_effector)

        for o in target_coll.all_objects:
            target_coll.objects.unlink(o) 
        bpy.data.collections.remove(target_coll)
        if self.keep_assets_coll == False:
            bpy.data.collections.remove(main_coll)
            

        # THOSE TWO LOOPS LOOKS USELESS BUT THEY ARE NECESSARY
        # IT'S A DUMB FIX BUT IT WORKS

        for col in objects_coll:
            if len(col.all_objects) > 0:
                while len(col.all_objects) > 1:
                    ob = col.all_objects[0]
                    if len(ob.users_collection) > 1:
                        col.objects.unlink(ob) 
                    else:
                        bpy.data.objects.remove(ob, do_unlink=True)
                        
        for col in objects_coll:
            if len(col.all_objects) > 0:
                ob = col.all_objects[0]
                if len(ob.users_collection) > 1:
                    col.objects.unlink(ob) 
                else:
                    bpy.data.objects.remove(ob, do_unlink=True)
            bpy.data.collections.remove(col)
            
        return {'FINISHED'}