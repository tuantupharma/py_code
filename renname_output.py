import bpy

# Get the active scene
scene = bpy.context.scene

# Loop through all nodes in the active scene's node tree
for node in scene.node_tree.nodes:

    # Check if the node is a File Output node
    if node.type == "OUTPUT_FILE":

        # Loop through all file slots in the node
        for slot in node.layer_slots:

            # Check if the slot path contains "Beauty"
            if "Beauty" in slot.name:

                # Change the slot path to include "RGBA"
                slot.name = slot.name.replace("Beauty", "RGBA")