import itertools
import math

import bpy
import bmesh
from bpy_extras.node_shader_utils import PrincipledBSDFWrapper


def ball_location_keyframes(b):
    # start point, where the ball lifts off the parent
    b.location = (0.0, -3.0, 0.0)
    b.keyframe_insert(data_path="location", frame=0)
    b.animation_data.action.fcurves[0].keyframe_points[-1].interpolation = "BEZIER"
    b.animation_data.action.fcurves[1].keyframe_points[-1].interpolation = "BEZIER"

    # mid point, the apex of the ball's flight
    b.location = (0.0, -1.5, 2.0)
    b.keyframe_insert(data_path="location", frame=10)
    b.animation_data.action.fcurves[1].keyframe_points[-1].handle_left_type = "VECTOR"
    b.animation_data.action.fcurves[1].keyframe_points[-1].handle_right_type = "VECTOR"

    # end point, where the ball lands on the child
    b.location = (0.0, 0.0, 0.0)
    b.keyframe_insert(data_path="location", frame=20)
    b.animation_data.action.fcurves[0].keyframe_points[-1].interpolation = "CONSTANT"
    b.animation_data.action.fcurves[0].keyframe_points[-1].handle_left_type = "FREE"
    b.animation_data.action.fcurves[0].keyframe_points[-1].handle_left[0] = 0.0
    b.animation_data.action.fcurves[1].keyframe_points[-1].interpolation = "CONSTANT"
    b.animation_data.action.fcurves[1].keyframe_points[-1].handle_left_type = "FREE"
    b.animation_data.action.fcurves[1].keyframe_points[-1].handle_left[1] = 0.0

    b.location = (0.0, 1.0, 0.0)
    b.keyframe_insert(data_path="location", frame=21)
    b.animation_data.action.fcurves[0].keyframe_points[-1].interpolation = "BEZIER"
    b.animation_data.action.fcurves[1].keyframe_points[-1].interpolation = "BEZIER"

    b.location = (0.0, 2.5, 2.0)
    b.keyframe_insert(data_path="location", frame=31)
    b.animation_data.action.fcurves[1].keyframe_points[-1].handle_left_type = "VECTOR"
    b.animation_data.action.fcurves[1].keyframe_points[-1].handle_right_type = "VECTOR"

    # end point, where the ball lands on the child
    b.location = (0.0, 4.0, -0.0)
    b.keyframe_insert(data_path="location", frame=41)
    b.animation_data.action.fcurves[0].keyframe_points[-1].interpolation = "CONSTANT"
    b.animation_data.action.fcurves[0].keyframe_points[-1].handle_left_type = "FREE"
    b.animation_data.action.fcurves[0].keyframe_points[-1].handle_left[0] = 0.0
    b.animation_data.action.fcurves[1].keyframe_points[-1].interpolation = "CONSTANT"
    b.animation_data.action.fcurves[1].keyframe_points[-1].handle_left_type = "FREE"
    b.animation_data.action.fcurves[1].keyframe_points[-1].handle_left[1] = 4.0

b = bpy.data.objects["ball.000"]
b.animation_data_clear()
ball_location_keyframes(b)


b = bpy.data.objects["ball.001"]
b.animation_data_clear()
# ball_location_keyframes(b)/

p = bpy.data.objects["path"]


b = bpy.data.objects['ball.000']
f = b.animation_data.action.fcurves[1].keyframe_points[2].interpolation
fcurves = b.animation_data.action.fcurves
for fcurve in fcurves:
    for kf in fcurve.keyframe_points:
        print(kf, kf.interpolation)
        print(kf.handle_left, kf.handle_right)
