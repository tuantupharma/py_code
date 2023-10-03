import bpy

# Create a new collection named "gpt_do"
new_collection = bpy.data.collections.new("gpt_do")
bpy.context.scene.collection.children.link(new_collection)

# Move currently selected objects to the new collection
selected_objects = bpy.context.selected_objects
for obj in selected_objects:
    new_collection.objects.link(obj)

# Check if the current selected objects are linked from other files
is_linked = all(obj.library for obj in selected_objects)

if is_linked:
    # If linked, duplicate the linked collections and their objects
    num_duplicates = 5
    offset = bpy.data.objects["b"].location  # Replace "b" with the object name to use as an offset

    for _ in range(num_duplicates):
        for obj in selected_objects:
            if obj.library:
                new_object = obj.copy()
                new_object.data = obj.data.copy()
                new_collection.objects.link(new_object)
                new_object.location += offset
else:
    # If not linked, duplicate the objects
    for _ in range(5):
        for obj in selected_objects:
            new_object = obj.copy()
            new_object.data = obj.data.copy()
            new_collection.objects.link(new_object)
