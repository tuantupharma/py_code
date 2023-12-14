import bpy
import time


# Set the name of the desired keymap
keymap_name = "Report Missing Files"

# Find the keymap with the specified name
keymap = None
for km in bpy.context.window_manager.keyconfigs.active.keymaps:
    if km.name == keymap_name:
        keymap = km
        break

if keymap is not None:
    # Trigger the custom shortcut to run the 'report_missing_files' operation
    for kmi in keymap.keymap_items:
        if kmi.idname == 'file.report_missing_files':
            bpy.ops.wm.context_set_int(data_path="space_data.type", value=1)  # Set the 3D View as the context
            kmi.idname = 'file.report_missing_files'
            kmi.context = 'INVOKE_DEFAULT'
            bpy.ops.wm.keymap_item_add(kmi)
            bpy.ops.file.report_missing_files('INVOKE_DEFAULT')
            bpy.ops.wm.keymap_item_remove({'active': kmi})
            bpy.ops.wm.context_set_int(data_path="space_data.type", value=2)  # Restore the context
            break

    print(f"Custom shortcut '{keymap_name}' triggered.")
else:
    print(f"Custom shortcut '{keymap_name}' not found in the active keymaps.")



# Wait for a few seconds to allow the report to be generated
time.sleep(12)  # You can adjust the delay time as needed

# Run the 'report_missing_files' operation
#bpy.ops.file.report_missing_files()


# Wait for a few seconds to allow the report to be generated
#time.sleep(15)  # You can adjust the delay time as needed


# Find the 'INFO' area in Blender
info_area = None
for window in bpy.context.window_manager.windows:
    for area in window.screen.areas:
        if area.type == 'INFO':
            info_area = area
            break
    if info_area:
        break

if info_area is not None:
    # Create a new context with the 'INFO' area as the active space
    override = bpy.context.copy()
    override['window'] = bpy.context.window
    override['screen'] = window.screen
    override['area'] = info_area

    # Select all reports in the 'INFO' area
    bpy.ops.info.select_all(override, action='SELECT')
    
    # Copy the reports to the clipboard
    bpy.ops.info.report_copy(override)

    # Retrieve the copied text
    clipboard_text = bpy.context.window_manager.clipboard

    # Export the copied reports to a text file
    file_path = "I:\\job\\HoaPhat\\text_ai\\missing_files_report.txt"
    with open(file_path, 'w') as file:
        file.write(clipboard_text)

    print(f"Reports in INFO area copied to {file_path}")
else:
    print("INFO area not found in the current screen layout.")
