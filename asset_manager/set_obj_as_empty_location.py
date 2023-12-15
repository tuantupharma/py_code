import bpy
for obj in bpy.context.scene.objects:
    if obj.type == 'EMPTY':
        empty = obj
        for child in empty.children:
            child.matrix_parent_inverse = empty.matrix_world.inverted()
