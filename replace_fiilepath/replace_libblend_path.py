import bpy

search_string = "\\\\192.168.0.7\\senshu\\JOBSTUDIO_2022\\"
replace_string = "T:\\"

for library in bpy.data.libraries:
    if search_string in library.filepath:
        library.filepath = library.filepath.replace(search_string, replace_string)
        print(f"Updated library path: {library.filepath}")
