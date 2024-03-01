import bpy

search_string = "\\\\192.168.0.7\\senshu\\JOBSTUDIO_2022\\"
replace_string = "T:\\"

for image in bpy.data.images:
    print(f"path: {image.filepath}")
    if search_string in image.filepath:
        image.filepath = image.filepath.replace(search_string, replace_string)
        print(f"Updated image path: {image.filepath}")
