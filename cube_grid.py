import itertools
import math
from random import randint

import bpy
import bmesh
from bpy_extras.node_shader_utils import PrincipledBSDFWrapper

# orange red (cover)
colors = [
    [0.787, 0.787, 0.787],
    [0.761, 0.716, 0.292],
    [1.000, 0.365, 0.084],
    [0.823, 0.117, 0.014],
    [0.983, 0.044, 0.0],
    [0.730, 0.030, 0.0],
    [0.448, 0.012, 0.0],
    [0.448, 0.012, 0.0]]

def add_cube(x, y, z, material):
    mesh = bpy.data.meshes.new("Cube")
    ob = bpy.data.objects.new("Cube", mesh)
    bpy.data.collections['cubes'].objects.link(ob)

    ob.select_set(state=True)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=0.9)
    bm.to_mesh(mesh)
    bm.free()
    # reposition
    bpy.ops.transform.resize(value=(1.0, 1.0, z))
    bpy.ops.transform.translate(value=(x, y, 0.9*z / 2))

    m = materials[min(math.floor(1.0*z), 8)]
    ob.data.materials.append(m)
    # deselect
    ob.select_set(state=False)

# Clear the scene
for ob in bpy.data.collections['cubes'].objects[:]:
    bpy.data.objects.remove(ob, do_unlink=True)


# deleting materials
for m in bpy.data.materials:
    if m.name.startswith("mat1."):
        print("deleting: " + m.name)
        bpy.data.materials.remove(m)

# setup materials
materials = []
for i, color in enumerate(colors):
    orig = bpy.data.materials["mat1"]
    m1 = orig.copy()
    m1.name = "mat1.%d" % i
    p = PrincipledBSDFWrapper(m1, is_readonly=False)
    p.base_color = color
    # print(m1.name, m1.diffuse_color[0], color, bpy.data.materials[new_name].diffuse_color[0])
    materials.append(m1)


# materials.reverse()



import csv
path = '/home/pboone/workspace/pm-blender/bins_alldof.csv'
# path = 'C:/Users/Paul Boone/Documents/Cover Art/bins_alldof.csv'
with open(path) as csvfile:
    rows = csv.reader(csvfile)
    for i, row in enumerate(rows):
        for j, num_materials in enumerate(row):
            if i < 20 and j < 20:
                weight = float(num_materials)
                if weight != 0:
                    weight = 2.0 * math.log(weight)
                add_cube(i, j, weight, "mat1")
