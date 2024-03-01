import bpy
import os
import csv

def list_missing_blend_libs():
    missing_libs = []
    for lib in bpy.data.libraries:
        try:
            lib_path = bpy.path.abspath(lib.filepath)
            if not os.path.exists(lib_path):
                missing_libs.append(lib_path)
                print(f"Missing library: {lib_path}")
        except Exception as e:
            print(f"Error processing library: {lib.filepath}, Error: {e}")
    return missing_libs

def list_missing_texture():
    missing_libs = []
    for lib in bpy.data.images:
        try:
            lib_path = bpy.path.abspath(lib.filepath)
            if not os.path.exists(lib_path):
                missing_libs.append(lib_path)
                print(f"Missing texture: {lib_path}")
        except Exception as e:
            print(f"Error processing texture: {lib.filepath}, Error: {e}")
    return missing_libs

def list_missing_clip():
    missing_libs = []
    for lib in bpy.data.movieclips:
        try:
            lib_path = bpy.path.abspath(lib.filepath)
            if not os.path.exists(lib_path):
                missing_libs.append(lib_path)
                print(f"Missing clip: {lib_path}")
        except Exception as e:
            print(f"Error processing clip: {lib.filepath}, Error: {e}")
    return missing_libs

# Call the function to get the list of missing blend libraries
missing_libs_blend = list_missing_blend_libs()

# Call the function to get the list of missing textures
missing_libs_texture = list_missing_texture()

# Call the function to get the list of missing clips
missing_libs_clip = list_missing_clip()

# Specify the CSV output paths for each type
csv_output_path_blend = 'C:\\Users\\Admin\\source\\repos\\bpython_automation\\dummydata\\missing_blend.csv'
csv_output_path_texture = 'C:\\Users\\Admin\\source\\repos\\bpython_automation\\dummydata\\missing_texture.csv'
csv_output_path_clip = 'C:\\Users\\Admin\\source\\repos\\bpython_automation\\dummydata\\missing_clip.csv'

# Write the missing blend libraries information to the CSV file
with open(csv_output_path_blend, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for lib in missing_libs_blend:
        writer.writerow([lib])
print(f"Missing blend libraries information written to: {csv_output_path_blend}")

# Write the missing textures information to the CSV file
with open(csv_output_path_texture, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for lib in missing_libs_texture:
        writer.writerow([lib])
print(f"Missing textures information written to: {csv_output_path_texture}")

# Write the missing clips information to the CSV file
with open(csv_output_path_clip, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for lib in missing_libs_clip:
        writer.writerow([lib])
print(f"Missing clips information written to: {csv_output_path_clip}")
