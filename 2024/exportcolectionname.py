import bpy
import csv
import os

def export_children_collections_to_csv(collection, blend_file_path):
    """
    Export names of all children collections within the given collection to a CSV file.

    Args:
    - collection: Blender collection object.
    - blend_file_path: Path to the Blender file.
    """
    # Get the directory of the blend file
    blend_file_dir = os.path.dirname(blend_file_path)
    csv_file_path = os.path.join(blend_file_dir, "tenfile.csv")

    with open(csv_file_path, mode='w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Collection Name"])

        for child_collection in collection.children:
            csv_writer.writerow([child_collection.name])

# Get the "Assets" collection
assets_collection = bpy.data.collections.get("Assets")

if assets_collection:
    # Get the path of the current blend file
    blend_file_path = bpy.data.filepath

    # Export children collection names to CSV
    export_children_collections_to_csv(assets_collection, blend_file_path)

    print("Children collection names exported to 'tenfile.csv'")
else:
    print("Assets collection not found")
