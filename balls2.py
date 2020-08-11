
import bpy
from bpy_extras.node_shader_utils import PrincipledBSDFWrapper
import bmesh

## hack to get cmocean to load right without tkintetr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import cmocean
import pandas as pd

# epsrange = (1.258, 513.26)
epsrange = (2.516-342.176)
def normalize_eps(eps):
    return (eps - epsrange[0]) / (epsrange[1] - epsrange[0])

def get_uccoords_atoms(csv_path):
    with open(csv_path, "r") as f:
        uc = [float(f) for f in next(f).split(":")[1].split(",")]
        points = pd.read_csv(f, skipinitialspace=True)
    return uc, points

def delete_materials():
    # deleting materials
    for m in bpy.data.materials:
        if m.name.startswith("pm1."):
            print("deleting: " + m.name)
            bpy.data.materials.remove(m)

def materialname(sig,eps):
    return "pm1.%f.%f" % (sig, eps)

def ballname(structure_id, id):
    return "Ball.%d.%d" % (structure_id, id)

def create_materials(points):
    cm = cmocean.cm.thermal
    # get all materials: unique combination of sigma and epsilon
    for sig, eps in set(zip(points.sigma, points.epsilon)):
        m = bpy.data.materials["pm1"].copy()
        m.name = materialname(sig, eps)
        p = PrincipledBSDFWrapper(m, is_readonly=False)
        p.base_color = cm(normalize_eps(eps))[0:3]

def add_ball(row):
    mesh = bpy.data.meshes.new(ballname(row.structure_id, row.id))
    ball = bpy.data.objects.new(ballname(row.structure_id, row.id), mesh)
    bpy.context.collection.objects.link(ball)
    ball.select_set(state=True)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=12, v_segments=12, diameter=row.sigma)
    bm.to_mesh(mesh)
    bm.free()
    bpy.ops.transform.translate(value=(row.x, row.y, row.z))
    bpy.ops.object.shade_smooth()
    ball.data.materials.append(bpy.data.materials[materialname(row.sigma, row.epsilon)])
    ball.select_set(state=False)

def select_ball(row):
    bpy.context.scene.objects[ballname(row.structure_id, row.id)].select_set(True)


def setup_array(arr, x, y, z, num):
    arr.constant_offset_displace = (x, y, z)
    arr.count = num
    arr.use_constant_offset = True
    arr.use_relative_offset = False

def extend_uc(obj, uc, num):
    setup_array(obj.modifiers.new("arrx", "ARRAY"), uc[0], 0.0, 0.0, 3)
    setup_array(obj.modifiers.new("arry", "ARRAY"), 0.0, uc[1], 0.0, 3)
    setup_array(obj.modifiers.new("arrz", "ARRAY"), 0.0, 0.0, uc[2], 3)

def load_material_csv(csv_path, setup_array=True):
    uc, points = get_uccoords_atoms(csv_path)
    points.x = points.x * uc[0]
    points.y = points.y * uc[1]
    points.z = points.z * uc[2]
    print(uc)
    print(points)
    bpy.ops.object.select_all(action='DESELECT')
    create_materials(points)
    points.apply(add_ball, axis=1)
    points.apply(select_ball, axis=1)
    bpy.context.view_layer.objects.active = bpy.context.scene.objects[ballname(points.iloc[0].structure_id, points.iloc[0].id)]
    if setup_array:
        bpy.ops.object.join()
        extend_uc(bpy.context.active_object, uc, 3)



# csv_path = "/Users/pboone/workspace/pm-blender/sample.csv"
load_material_csv("/Users/pboone/workspace/htsohm/2848.csv")
load_material_csv("/Users/pboone/workspace/htsohm/2066.csv")
load_material_csv("/Users/pboone/workspace/htsohm/2911.csv")
load_material_csv("/Users/pboone/workspace/htsohm/2843.csv")
load_material_csv("/Users/pboone/workspace/htsohm/9811.csv")
load_material_csv("/Users/pboone/workspace/htsohm/6415.csv")
load_material_csv("/Users/pboone/workspace/htsohm/9149.csv")
load_material_csv("/Users/pboone/workspace/htsohm/7120.csv")
load_material_csv("/Users/pboone/workspace/htsohm/7846.csv")
load_material_csv("/Users/pboone/workspace/htsohm/7844.csv")
