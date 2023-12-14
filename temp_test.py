import bpy



# Reset the Armature to the default POSE.


for n in bpy.context.object.pose.bones:
    n.location = (0, 0, 0)
    n.rotation_quaternion = (1, 0, 0, 0)
    n.rotation_axis_angle = (0, 0, 1, 0)
    n.rotation_euler = (0, 0, 0)
    n.scale = (1, 1, 1)