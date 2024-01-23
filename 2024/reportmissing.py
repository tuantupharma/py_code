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
                print(f"Missing library: {lib_path}")
        except Exception as e:
            print(f"Error processing library: {lib.filepath}, Error: {e}")
    return missing_libs

# Call the function to get the list of missing blend libraries
missing_libs = list_missing_blend_libs()

# Specify the CSV output path
csv_output_path = 'C:\\Users\\Admin\\source\\repos\\bpython_automation\\dummydata\\missing.csv'

# Write the missing blend libraries information to the CSV file
with open(csv_output_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for lib in missing_libs:
        writer.writerow([lib])
        
missing_libs = list_missing_texture()
        
with open(csv_output_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for lib in missing_libs:
        writer.writerow([lib])

print(f"Missing blend libraries information written to: {csv_output_path}")
