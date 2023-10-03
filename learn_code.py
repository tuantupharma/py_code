import bpy


class OBJECT_OT_make_test_camera(bpy.types.Operator):
    """Make a test camera"""
    bl_idname = "object.make_test_camera"
    bl_label = "Make Test Camera"

    @classmethod
    def poll(cls, context):
        return bpy.ops.view3d.camera_to_view.poll()

    def execute(self, context):
        cameraName = "SimpleRenderCam"
        cam = bpy.data.cameras.new(cameraName)
        cam.lens = 90
        cameraObject = bpy.data.objects.new(cameraName, cam)
        context.scene.collection.objects.link(cameraObject)
        context.scene.camera = cameraObject
        print(context.area.type)
        bpy.ops.view3d.camera_to_view()
        return{'FINISHED'}


class VIEW_3D_PT_test_camera(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Test Camera"
    bl_label = "Create camera to test area"
    # bl_context = "object"

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.label(text="View type is:")
        row.label(text=f"{context.area.type}")

        row = layout.row()
        row.operator('object.make_test_camera')


def register():
    bpy.utils.register_class(VIEW_3D_PT_test_camera)
    bpy.utils.register_class(OBJECT_OT_make_test_camera)


def unregister():
    bpy.utils.unregister_class(VIEW_3D_PT_test_camera)
    bpy.utils.unregister_class(OBJECT_OT_make_test_camera)


if __name__ == "__main__":
    register()