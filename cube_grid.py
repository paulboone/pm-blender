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
#
# # orange red
# colors = [
#     [1.        , 0.96862745, 0.9254902 ],
#     [0.99607843, 0.90980392, 0.78431373],
#     [0.99215686, 0.83137255, 0.61960784],
#     [0.99215686, 0.73333333, 0.51764706],
#     [0.98823529, 0.55294118, 0.34901961],
#     [0.9372549 , 0.39607843, 0.28235294],
#     [0.84313725, 0.18823529, 0.12156863],
#     [0.70196078, 0.        , 0.        ],
#     [0.49803922, 0.        , 0.        ]]

# # yellow orange red
# colors = [
#  [1.        , 1.        , 0.8       ],
#  [1.        , 0.92941176, 0.62745098],
#  [0.99607843, 0.85098039, 0.4627451 ],
#  [0.99607843, 0.69803922, 0.29803922],
#  [0.99215686, 0.55294118, 0.23529412],
#  [0.98823529, 0.30588235, 0.16470588],
#  [0.89019608, 0.10196078, 0.10980392],
#  [0.74117647, 0.        , 0.14901961],
#  [0.50196078, 0.        , 0.01176471]]
#
# # mono green
# colors = [
#  [0.96862745, 0.98823529, 0.96078431],
#  [0.89803922, 0.96078431, 0.87843137],
#  [0.78039216, 0.91372549, 0.75294118],
#  [0.63137255, 0.85098039, 0.60784314],
#  [0.45490196, 0.76862745, 0.4627451 ],
#  [0.25490196, 0.67058824, 0.36470588],
#  [0.1372549 , 0.54509804, 0.27058824],
#  [0.        , 0.42745098, 0.17254902],
#  [0.        , 0.26666667, 0.10588235]]
#
# # mono orange 6
# colors = [
#  [0.99607843, 0.92941176, 0.87058824],
#  [0.99215686, 0.81568627, 0.63529412],
#  [0.99215686, 0.68235294, 0.41960784],
#  [0.99215686, 0.55294118, 0.23529412],
#  [0.90196078, 0.33333333, 0.05098039],
#  [0.65098039, 0.21176471, 0.01176471]]

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
path = '/home/pboone/Blender Documents/Cover Art/bins_alldof.csv'
path = 'C:/Users/Paul Boone/Documents/Cover Art/bins_alldof.csv'
with open(path) as csvfile:
    rows = csv.reader(csvfile)
    for i, row in enumerate(rows):
        for j, num_materials in enumerate(row):
            if i < 20 and j < 20:
                weight = float(num_materials)
                if weight != 0:
                    weight = 2.0 * math.log(weight)
                add_cube(i, j, weight, "mat1")
