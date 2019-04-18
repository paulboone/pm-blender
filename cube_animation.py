import csv
import itertools
import math
from random import randint
import time

import bpy
import bmesh
from bpy_extras.node_shader_utils import PrincipledBSDFWrapper
import numpy as np

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

def init_cube_material(x, y):
    orig = bpy.data.materials["mat1"]
    m = orig.copy()
    m.name = "mat1_%d_%d" % (x, y)
    p = PrincipledBSDFWrapper(m, is_readonly=False)
    p.base_color = colors[0]
    return m

def init_cube(x, y):
    mesh = bpy.data.meshes.new("Cube")
    ob = bpy.data.objects.new("Cube_%d_%d" % (x, y), mesh)
    bpy.data.collections['cubes'].objects.link(ob)

    ob.select_set(state=True)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=0.9)
    bm.to_mesh(mesh)
    bm.free()
    # reposition
    bpy.ops.transform.resize(value=(1.0, 1.0, 0.0))
    bpy.ops.transform.translate(value=(x, y, 0)) # 0.9*z / 2)

    m = init_cube_material(x, y)
    ob.data.materials.append(m)
    # deselect
    ob.select_set(state=False)

def animate_cube_height(x, y, z, sf, ef):
    obj = bpy.data.objects["Cube_%d_%d" % (x, y)]
    m = bpy.data.materials["mat1_%d_%d" % (x, y)]
    bsdf_shader = m.node_tree.nodes.get("Principled BSDF").inputs[0]
    obj.keyframe_insert(data_path="scale", frame=sf, index=2)
    obj.keyframe_insert(data_path="location", frame=sf, index=2)
    bsdf_shader.keyframe_insert(data_path='default_value', frame=sf)

    if z == -1:
        z = obj.scale[2] + 1
    color = colors[min(math.floor(1.0*z), 7)] + [1.0]
    obj.scale[2] = z
    obj.location[2] = 0.9*z/2
    bsdf_shader.default_value = color

    obj.keyframe_insert(data_path="scale", frame=ef, index=2)
    obj.keyframe_insert(data_path="location", frame=ef, index=2)
    bsdf_shader.keyframe_insert(data_path='default_value', frame=ef)

def delete_all_scene():
    # Clear the scene
    t1 = time.perf_counter()
    for ob in bpy.data.collections['cubes'].objects[:]:
        bpy.data.objects.remove(ob, do_unlink=True)

    t2 = time.perf_counter()
    print("Time to delete cubes: %f" % (t2 - t1))
    # deleting materials
    for m in bpy.data.materials:
        if m.name.startswith("mat1.") or m.name.startswith("mat1_"):
            # print("deleting: " + m.name)
            bpy.data.materials.remove(m)

    t3 = time.perf_counter()
    print("Time to delete materials: %f" % (t3 - t2))

# pm_datacsv_path = '/home/pboone/workspace/pm-blender/bins_alldof.csv'
# path = 'C:/Users/Paul Boone/Documents/Cover Art/bins_alldof.csv'

def init_scene(x, y):
    for i in range(x):
        for j in range(y):
            init_cube(i, j)
#
# def load_scene(path):
#     with open(path) as csvfile:
#         rows = csv.reader(csvfile)
#         for i, row in enumerate(rows):
#             for j, num_materials in enumerate(row):

#
delete_all_scene()

t1 = time.perf_counter()
init_scene(8,8)
t2 = time.perf_counter()
print("Time to create: %f" % (t2 - t1))

anim_gens = np.load("/home/pboone/workspace/pm-blender/animation.npy")

for i, gen in enumerate(anim_gens):
    for mats in gen:
        x, y, px, py = mats
        if x < 8 and y < 8:
            animate_cube_height(x, y, -1, i * 10, (i + 1) * 10)

#
# for i in range(36):
#     animate_cube_height(i + 2, i, 4, 20, 30)
#
# for i in range(36):
#     animate_cube_height(i + 2, i, 6, 30, 40)
