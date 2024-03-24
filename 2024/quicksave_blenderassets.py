import bpy
import os
import csv
from datetime import datetime

class QuickSaveModelFile(bpy.types.Operator):
    bl_idname = "model.quick_save_file"
    bl_label = "Quick Save Model File"

    def execute(self, context):
        # Get the active collection
        active_collection = bpy.context.view_layer.active_layer_collection.collection

        # Check if the collection name contains " Collection"
        collection_name = active_collection.name
        if " Collection" not in collection_name:
            # Generate file name based on the collection name
            file_name = collection_name + ".blend"

            # Define output folder path
            output_folder = "D:\\job\\upload_assets\\model_lib"

            # Set file path
            file_path = os.path.join(output_folder, file_name)

            # Save the Blender file
            bpy.ops.wm.save_as_mainfile(filepath=file_path)

            # Create text datablock with information
            text_block = bpy.data.texts.new(name="Information")
            text_block.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            text_block.write(f"PC Name: {os.environ.get('COMPUTERNAME')}\n")
            text_block.write("Version: 1.0\n")
            text_block.write("QC Checked: No\n")

            # Create CSV file with information
            csv_file_path = os.path.join(output_folder, "model_info.csv")
            with open(csv_file_path, mode='w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["File Name", "Date", "PC Name", "Version", "QC Checked"])
                csv_writer.writerow([file_name, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), os.environ.get('COMPUTERNAME'), "1.0", "No"])

            self.report({'INFO'}, f"File saved as '{file_name}'")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Collection name contains ' Collection'. Please select a different collection.")
            return {'CANCELLED'}

def register():
    bpy.utils.register_class(QuickSaveModelFile)

def unregister():
    bpy.utils.unregister_class(QuickSaveModelFile)

if __name__ == "__main__":
    register()
