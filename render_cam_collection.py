bl_info = {
    "name": "Render Cam Collection",
    "blender": (2, 80, 0),
    "category": "Render",
}

import bpy
from bpy.types import Panel

class RENDER_OT_RenderCamCollection(bpy.types.Operator):
    bl_idname = "render.cam_collection"
    bl_label = "Render Cam Collection"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Get the collection name from the text box
        output_folder = bpy.context.scene.my_tool.output_folder

        # Specify the name of the collection containing the cameras
        camera_collection_name = "camera"

        # Get the collection by name
        camera_collection = bpy.data.collections.get(camera_collection_name)

        # Check if the collection exists
        if camera_collection:
            # Get the list of all cameras in the collection
            cameras = [obj for obj in camera_collection.objects if obj.type == 'CAMERA']

            # Loop through each camera and render
            for camera in cameras:
                # Set the active camera
                bpy.context.scene.camera = camera
                
                # Set the output file path for the rendered image
                render_settings = bpy.context.scene.render
                render_settings.filepath = f"{output_folder}/{camera.name}"

                # Render the image
                bpy.ops.render.render(write_still=True)
                
                # Optionally, you can print a message to indicate that the rendering is complete
                print(f"Rendered image from camera: {camera.name}")

            # Optionally, reset the active camera to the default camera (e.g., "Camera")
            bpy.context.scene.camera = bpy.data.objects["Camera"]
        else:
            print(f"Collection '{camera_collection_name}' not found.")

        return {'FINISHED'}

class MyAddonProperties(bpy.types.PropertyGroup):
    output_folder: bpy.props.StringProperty(
        name="Output Folder",
        default="/path/to/output/folder",
        description="Choose the folder where rendered images will be saved."
    )

def draw_func(self, context):
    layout = self.layout
    scene = context.scene

    # Create a box for the addon settings
    box = layout.box()
    box.label(text="Render Cam Collection Settings")

    # Add a text box to choose the output folder
    box.prop(scene.my_tool, "output_folder", text="Output Folder")

    # Add a button to trigger the rendering
    box.operator("render.cam_collection", text="Render Cam Collection")

def register():
    bpy.utils.register_class(RENDER_OT_RenderCamCollection)
    bpy.utils.register_class(MyAddonProperties)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=MyAddonProperties)
    bpy.types.TOPBAR_HT_upper_bar.prepend(draw_func)

def unregister():
    bpy.utils.unregister_class(RENDER_OT_RenderCamCollection)
    bpy.utils.unregister_class(MyAddonProperties)
    del bpy.types.Scene.my_tool
    bpy.types.TOPBAR_HT_upper_bar.remove(draw_func)

if __name__ == "__main__":
    register()
