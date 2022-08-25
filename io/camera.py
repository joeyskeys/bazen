
import bpy
import mathutils
import math
import xml.etree.ElementTree as ET
from .base import BaseIO


class CameraIO(BaseIO):
    """

    """

    def __init__(self):
        pass

    def get_camera_infos(self):
        active_camera = bpy.context.scene.camera
        camera_matrix = active_camera.matrix_world
        eye_pos = camera_matrix.translation
        look_vec = mathutils.Vector((0, 0, -1))
        look_vec.rotate(camera_matrix.to_3x3())
        up_vec = mathutils.Vector((0, 1, 0))
        up_vec.rotate(camera_matrix.to_3x3())
        return eye_pos, look_vec, up_vec

    def get_fov(self):
        return bpy.context.scene.camera.data.angle

    def get_props(self):
        return bpy.context.scene.bitto_camera_props

    def write_description(self, handle):
        pos, look_vec, up_vec = self.get_camera_infos()
        look_at = pos + look_vec
        fov = self.get_fov()
        props = (' '.join(map(str, [pos.x, pos.z, -pos.y])), ' '.join(map(str, [look_at.x, look_at.z, -look_at.y])), ' '.join(map(str, [up_vec.x, up_vec.z, -up_vec.y])), str(fov))
        prop_strs = map(' '.join, zip(['float3'] * 3 + ['float'], props))
        prop_dict = dict(zip(('position', 'lookat', 'up', 'fov'), prop_strs))
        camera_node = ET.SubElement(handle, 'Camera', prop_dict)

    def feed_api(self):
        pass
