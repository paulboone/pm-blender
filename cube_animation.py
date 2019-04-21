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

def animate_cube_height(x, y, z, sequence_start, offset, alength):
    sf = sequence_start + offset
    ef = sf + alength
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

def animate_highlighters(mats, sequence_start, offset, alength):
    sf = sequence_start + offset
    ef = sf + alength
    for i, mat in enumerate(mats):
        _, _, px, py = mat
        # print("pxpy %d %d" % (px, py))
        cube = bpy.data.objects["Cube_%d_%d" % (px, py)]
        ob = bpy.data.objects["hl.%03d" % i]
        ob.keyframe_insert(data_path="location", frame=sf)
        ob.location = (px, py, cube.scale[2] * 0.9 + 0.05)
        ob.keyframe_insert(data_path="location", frame=ef)

def ball_location_keyframes(b, pt_start, pt_end, sequence_start, offset, alength):
    sf = sequence_start + offset
    ef = sf + alength
    mf = (sf + ef) / 2
    pt_mid = ((pt_end[0] + pt_start[0])/2, (pt_end[1] + pt_start[1])/2, 5.0)

    # start point, where the ball lifts off the parent
    b.location = pt_start
    b.keyframe_insert(data_path="location", frame=sf)
    b.animation_data.action.fcurves[0].keyframe_points[-1].interpolation = "BEZIER"
    b.animation_data.action.fcurves[0].keyframe_points[-1].handle_right_type = "FREE"
    b.animation_data.action.fcurves[0].keyframe_points[-1].handle_right = (sf + 4.0, pt_start[0])
    b.animation_data.action.fcurves[1].keyframe_points[-1].interpolation = "BEZIER"
    b.animation_data.action.fcurves[1].keyframe_points[-1].handle_right_type = "FREE"
    b.animation_data.action.fcurves[1].keyframe_points[-1].handle_right = (sf + 4.0, pt_start[1])

    # mid point, the apex of the ball's flight
    b.location = pt_mid
    b.keyframe_insert(data_path="location", frame=mf)
    b.animation_data.action.fcurves[1].keyframe_points[-1].handle_left_type = "VECTOR"
    b.animation_data.action.fcurves[1].keyframe_points[-1].handle_right_type = "VECTOR"

    # end point, where the ball lands on the child
    b.location = pt_end
    b.keyframe_insert(data_path="location", frame=ef-1)
    print("before: ", b.animation_data.action.fcurves[1].keyframe_points[-1].handle_left)
    b.animation_data.action.fcurves[0].keyframe_points[-1].interpolation = "CONSTANT"
    b.animation_data.action.fcurves[0].keyframe_points[-1].handle_left_type = "FREE"
    b.animation_data.action.fcurves[0].keyframe_points[-1].handle_left = (ef - 1 - 4.0, pt_end[0])
    b.animation_data.action.fcurves[1].keyframe_points[-1].interpolation = "CONSTANT"
    b.animation_data.action.fcurves[1].keyframe_points[-1].handle_left_type = "FREE"
    b.animation_data.action.fcurves[1].keyframe_points[-1].handle_left = (ef - 1 - 4.0, pt_end[1])
    print("after: ", b.animation_data.action.fcurves[1].keyframe_points[-1].handle_left)


def animate_balls(mats, sequence_start, offset, alength):
    sf = sequence_start + offset
    ef = sf + alength
    ball_diameter = 0.4

    for i, mat in enumerate(mats):
        x, y, px, py = mat
        cube = bpy.data.objects["Cube_%d_%d" % (x, y)]
        pcube = bpy.data.objects["Cube_%d_%d" % (px, py)]
        b = bpy.data.objects["ball.%03d" % i]
        pt_start = (px, py, pcube.scale[2] * 0.9 - ball_diameter)
        pt_end = (x, y, cube.scale[2] * 0.9 - ball_diameter)
        ball_location_keyframes(b, pt_start, pt_end, sequence_start, offset, alength)

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

def reset_highlighters():
    for i in range(10):
        ob = bpy.data.objects["hl.%03d" % i]
        ob.animation_data_clear()
        ob.location = (-1.0, -1.0, 0.0)

def reset_balls():
    for i in range(10):
        ob = bpy.data.objects["ball.%03d" % i]
        ob.animation_data_clear()
        ob.location = (-2.0, -3.0, 0.0)
        ob.keyframe_insert(data_path="location", frame=0)
        ob.animation_data.action.fcurves[0].keyframe_points[-1].interpolation = "CONSTANT"
        ob.animation_data.action.fcurves[1].keyframe_points[-1].interpolation = "CONSTANT"

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

bpy.context.scene.frame_set(0)
delete_all_scene()
reset_highlighters()
reset_balls()
sx = 8
sy = 8
t1 = time.perf_counter()
init_scene(sx, sy)
t2 = time.perf_counter()
print("Time to create: %f" % (t2 - t1))

anim_gens = np.load("/home/pboone/workspace/pm-blender/animation.npy")

gf = 60

for i, gen in enumerate(anim_gens):
    # bpy.context.scene.frame_set(i*gf)
    j = i + 1
    mats = [(mat[0] % sx, mat[1] % sy, mat[2] % sx, mat[3] % sy) for mat in gen]
    animate_highlighters(mats, j*gf, 0, 10)
    if i > 0:
        animate_balls(mats, j*gf, 10, 40)
    mat_moves = dict_count([(m[0],m[1]) for m in mats])
    for (x,y), z in mat_moves.items():
        animate_cube_height(x, y, -z, j*gf, 50, 10)
