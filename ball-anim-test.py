import itertools
import math

import bpy
import bmesh
from bpy_extras.node_shader_utils import PrincipledBSDFWrapper


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



b = bpy.data.objects["ball.000"]
b.animation_data_clear()
ball_location_keyframes(b, (0.0, 0.0, 0.0), (0.0, 2.0, 0.0), 0, 0, 20)
ball_location_keyframes(b, (0.0, 2.0, 0.0), (0.0, 4.0, 0.0), 20, 0, 20)
ball_location_keyframes(b, (0.0, 2.0, 0.0), (0.0, 4.0, 0.0), 40, 0, 20)
