import bpy
import csv
# TODO
# Function to create rendersetup.csv
def create_render_setup_file(render_setup, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['start_frame', 'end_frame', 'output_format', 'datetime', 'blender_file']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for setup in render_setup:
            writer.writerow(setup)

# Example render setup details
render_setup_details = [
    {'start_frame': 1, 'end_frame': 100, 'output_format': 'PNG', 'datetime': '2024-03-27 10:00:00', 'blender_file': 'scene1.blend'},
    {'start_frame': 101, 'end_frame': 200, 'output_format': 'PNG', 'datetime': '2024-03-27 10:00:00', 'blender_file': 'scene2.blend'},
    {'start_frame': 201, 'end_frame': 300, 'output_format': 'PNG', 'datetime': '2024-03-27 10:00:00', 'blender_file': 'scene3.blend'},
]

# Output file path
output_file_path = "S:\\rendermanager\\render\\rendersetup.csv"

# Create rendersetup.csv file
create_render_setup_file(render_setup_details, output_file_path)
