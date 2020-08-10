
import bpy
from bpy_extras.node_shader_utils import PrincipledBSDFWrapper
import bmesh

## hack to get cmocean to load right without tkintetr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import cmocean
import pandas as pd

epsrange = (1.258, 513.26)
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

def create_materials(points):
    cm = cmocean.cm.thermal
    # get all materials: unique combination of sigma and epsilon
    for sig, eps in set(zip(points.sigma, points.epsilon)):
        m = bpy.data.materials["pm1"].copy()
        m.name = materialname(eps, sig)
        p = PrincipledBSDFWrapper(m, is_readonly=False)
        p.base_color = cm(normalize_eps(eps))[0:3]

def add_ball(row):
    mesh = bpy.data.meshes.new("Ball")
    ball = bpy.data.objects.new("Ball", mesh)
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

csv_path = "/Users/pboone/workspace/pm-blender/sample.csv"
uc, points = get_uccoords_atoms(csv_path)

points.apply(add_ball, axis=1)

# mname =
# bpy.data.materials.new(mname)
# bpy.data.materials[mname].diffuse_color =
