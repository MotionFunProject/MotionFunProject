import bpy
import os
from math import radians
import time

print("Items in scene: " + str(len(bpy.context.scene.objects)));
bpy.ops.mesh.primitive_monkey_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(
True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
False, False, False))
bpy.ops.object.shade_smooth();
bpy.ops.object.modifier_add(type='SUBSURF');
bpy.context.object.modifiers["Subsurf"].levels = 3
context = bpy.context
scene = context.scene
ob = scene.objects.active
# ob.rotation_euler = (0, 0, radians(20))

dir_path = os.path.dirname(os.path.realpath(__file__))
print (dir_path)
f = open("/Users/juancarlosnavarrete/Desktop/BlenderEnv/cor.txt", "r")

for line in f:
    inner_list = [float(elt.strip()) for elt in line.split(',')]

positions = [];
# set up motion of the monkey
i = 0;
while i < len(inner_list):
    a, b, c = inner_list[i], inner_list[i + 1], inner_list[i + 2];
    i = i + 3;
    arr = [a, b, c];
    positions.append(arr);

ob = bpy.context.active_object
frame_num = 0

for position in positions:
    bpy.context.scene.frame_set(frame_num)
    ob.location = position
    print(position)
    ob.keyframe_insert(data_path="location", index=-1)
    frame_num += 10

f.close()

print('file is close')