import bpy
from bpy.types import Operator, Panel
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper

# Define the render operator
class RENDER_OT_RenderCamCollection(Operator):
    bl_idname = "render.render_cam_collection"
    bl_label = "Render Cam Collection"
    
    output_folder: StringProperty(
        name="Output Folder",
        subtype='DIR_PATH',
    )

    def execute(self, context):
        # Get the collection by name
        camera_collection_name = "camera"
        camera_collection = bpy.data.collections.get(camera_collection_name)

        if camera_collection:
            # Get the list of all cameras in the collection
            cameras = [obj for obj in camera_collection.objects if obj.type == 'CAMERA']

            # Loop through each camera and render
            for camera in cameras:
                # Set the active camera
                bpy.context.scene.camera = camera

                # Set the output file path for the rendered image
                render_settings = bpy.context.scene.render
                render_settings.filepath = f"{self.output_folder}/{camera.name}"

                # Render the image
                bpy.ops.render.render(write_still=True)

            # Optionally, reset the active camera to the default camera (e.g., "Camera")
            bpy.context.scene.camera = bpy.data.objects["Camera"]
        else:
            self.report({'ERROR'}, f"Collection '{camera_collection_name}' not found.")
        
        return {'FINISHED'}

# Define the render panel
class RENDER_PT_RenderCamCollectionPanel(Panel):
    bl_label = "Render Cam Collection"
    bl_idname = "RENDER_PT_RenderCamCollection"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout
        
        # Add a text box for choosing the output folder
        layout.label(text="Output Folder:")
        layout.prop(context.scene, "render_cam_collection_output_folder", text="")

        # Add a button to trigger the render operator
        layout.operator("render.render_cam_collection", text="Render Cam Collection")

def register():
    bpy.utils.register_class(RENDER_OT_RenderCamCollection)
    bpy.utils.register_class(RENDER_PT_RenderCamCollectionPanel)
    bpy.types.Scene.render_cam_collection_output_folder = StringProperty(
        name="Output Folder",
        subtype='DIR_PATH',
        default="",
    )

def unregister():
    bpy.utils.unregister_class(RENDER_OT_RenderCamCollection)
    bpy.utils.unregister_class(RENDER_PT_RenderCamCollectionPanel)
    del bpy.types.Scene.render_cam_collection_output_folder

if __name__ == "__main__":
    register()
