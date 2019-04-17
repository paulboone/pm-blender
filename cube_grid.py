import itertools
import math
from random import randint

import bpy
import bmesh
from bpy_extras.node_shader_utils import PrincipledBSDFWrapper

colors = [
 [1.        , 1.        , 0.85098039],
 [0.92941176, 0.97254902, 0.69411765],
 [0.78039216, 0.91372549, 0.70588235],
 [0.49803922, 0.80392157, 0.73333333],
 [0.25490196, 0.71372549, 0.76862745],
 [0.11372549, 0.56862745, 0.75294118],
 [0.13333333, 0.36862745, 0.65882353],
 [0.14509804, 0.20392157, 0.58039216],
 [0.03137255, 0.11372549, 0.34509804]]

colors = [
    [1.        , 0.96862745, 0.9254902 ],
    [0.99607843, 0.90980392, 0.78431373],
    [0.99215686, 0.83137255, 0.61960784],
    [0.99215686, 0.73333333, 0.51764706],
    [0.98823529, 0.55294118, 0.34901961],
    [0.9372549 , 0.39607843, 0.28235294],
    [0.84313725, 0.18823529, 0.12156863],
    [0.70196078, 0.        , 0.        ],
    [0.49803922, 0.        , 0.        ]]



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

    m = materials[math.floor(z)]
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
with open('/home/pboone/Blender Documents/Cover Art/bins_alldof.csv') as csvfile:
    rows = csv.reader(csvfile)
    for i, row in enumerate(rows):
        for j, num_materials in enumerate(row):
            if i < 8 and j < 8:
                weight = float(num_materials)
                if weight != 0:
                    weight = 2 * math.log(weight)
                add_cube(i, j, weight, "mat1")
