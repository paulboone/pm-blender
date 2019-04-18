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

    if z < 0: # do a positive relative offset if a negative z passed
        rawz = math.exp(obj.scale[2]) - z
        z = math.log(rawz)
    color = colors[min(math.floor(z + 1), 7)] + [1.0]
    obj.scale[2] = z
    obj.location[2] = 0.9*z/2
    bsdf_shader.default_value = color

    obj.keyframe_insert(data_path="scale", frame=ef, index=2)
    obj.keyframe_insert(data_path="location", frame=ef, index=2)
    bsdf_shader.keyframe_insert(data_path='default_value', frame=ef)

def animate_highlighters(mats, sf, ef):
    for i, mat in enumerate(mats):
        _, _, px, py = mat
        print("pxpy %d %d" % (px, py))
        cube = bpy.data.objects["Cube_%d_%d" % (px, py)]
        ob = bpy.data.objects["hl.%03d" % i]
        ob.keyframe_insert(data_path="location", frame=sf)
        ob.location = (px, py, cube.scale[2])
        ob.keyframe_insert(data_path="location", frame=ef)

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

def dict_count(l):
    result_dict = {}
    for a in l:
        if a in result_dict:
            result_dict[a] += 1
        else:
            result_dict[a] = 1
    return result_dict

def remove_all_keyframes():
    t1 = time.perf_counter()
    bpy.context.scene.frame_set(1)
    for ob in bpy.data.collections['cubes'].objects[:]:
        ob.animation_data_clear()
        ob.scale[2] = 0.0
        ob.location[2] = 0.0

    for m in bpy.data.materials:
        if m.name.startswith("mat1.") or m.name.startswith("mat1_"):
            bsdf_shader = m.node_tree.nodes.get("Principled BSDF").inputs[0]
            bsdf_shader.keyframe_delete(data_path='default_value')
            # m.animation_data_clear()

delete_all_scene()
sx = 8
sy = 8
t1 = time.perf_counter()
init_scene(sx, sy)
t2 = time.perf_counter()
print("Time to create: %f" % (t2 - t1))

anim_gens = np.load("/home/pboone/workspace/pm-blender/animation.npy")

gf = 30

for i, gen in enumerate(anim_gens):
    # bpy.context.scene.frame_set(i*gf)

    mats = [(mat[0] % sx, mat[1] % sy, mat[2] % sx, mat[3] % sy) for mat in gen]
    animate_highlighters(mats, i*gf, i*gf + 10)

    mat_moves = dict_count([(m[0],m[1]) for m in mats])
    for (x,y), z in mat_moves.items():
        animate_cube_height(x, y, -z, i*gf + 10, i*gf + gf)

#
# for i in range(36):
#     animate_cube_height(i + 2, i, 4, 20, 30)
#
# for i in range(36):
#     animate_cube_height(i + 2, i, 6, 30, 40)
