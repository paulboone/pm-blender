from random import randint

import bpy
import bmesh

import numpy as np

def add_ball(x, y, z, material):
    mesh = bpy.data.meshes.new("Ball")
    ball = bpy.data.objects.new("Ball", mesh)
    bpy.context.collection.objects.link(ball)
    ball.select_set(state=True)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=12, v_segments=12, diameter=1)
    bm.to_mesh(mesh)
    bm.free()
    # Reposition the ball
    bpy.ops.transform.translate(value=(x, y, z))
    # Apply smooth shading
    bpy.ops.object.shade_smooth()

    ball.data.materials.append(bpy.data.materials[material])
    # Deselect the ball
    ball.select_set(state=False)

# Clear the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Clear all materials
for m in bpy.data.materials:
    bpy.data.materials.remove(m)

# create materials

print("HI")

colors = [(229.0/255,109.0/255,057.0/255, 1.0), \
            (055.0/255,063.0/255,081.0/255, 1.0),\
            (126.0/255,189.0/255,195.0/255, 1.0),\
            (122.0/255,098.0/255,099.0/255, 1.0),\
            (138.0/255,203.0/255,136.0/255, 1.0)]

bpy.data.materials.new("A_0")
bpy.data.materials["A_0"].diffuse_color = colors[0]

bpy.data.materials.new("A_1")
bpy.data.materials["A_1"].diffuse_color = colors[1]

bpy.data.materials.new("A_2")
bpy.data.materials["A_2"].diffuse_color = colors[2]

bpy.data.materials.new("A_3")
bpy.data.materials["A_3"].diffuse_color = colors[3]

bpy.data.materials.new("A_4")
bpy.data.materials["A_4"].diffuse_color = colors[4]


structure_id = 1
uc_coords = [(40.711698678505, 46.1981552332081, 33.2260720548841), \
            (38.9690239804632, 28.8409855726316, 26.991504254944), \
            (42.4462853771919, 42.7620528736042, 47.4697832707382), \
            (27.5041948023392, 44.1736849686374, 28.7461229826881)]

ucx, ucy, ucz = uc_coords[structure_id - 1]


import csv
with open('/home/pboone/Blender Documents/Cover Art/sites1lim.txt') as csvfile:
    sites = csv.reader(csvfile, delimiter='|', quotechar='|')
    next(sites)
    for site in sites:
        atom_type, x, y, z = site[1:5]
        atom_structure_id = int(site[6])
        if atom_structure_id == structure_id:
            print(atom_type, x, y, z)
            add_ball(ucx*float(x), ucy*float(y),ucz*float(z), atom_type)
