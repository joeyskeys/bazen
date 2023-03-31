
import bpy
import mathutils
import math
import xml.etree.ElementTree as ET
from .base import BaseIO
from ..pyzen import vec as pv


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
        look_at = eye_pos + look_vec
        return eye_pos, look_at, up_vec

    def get_fov(self):
        return bpy.context.scene.camera.data.angle

    def get_props(self):
        return bpy.context.scene.camera.data.bitto_camera_props

    def write_description(self, handle):
        pos, look_at, up_vec = self.get_camera_infos()
        fov = self.get_fov() / math.pi * 180
        props = (' '.join(map(str, [pos.x, pos.z, -pos.y])), ' '.join(map(str, [look_at.x, look_at.z, -look_at.y])), ' '.join(map(str, [up_vec.x, up_vec.z, -up_vec.y])), str(fov))
        prop_strs = map(' '.join, zip(['float3'] * 3 + ['float'], props))
        prop_dict = dict(zip(('position', 'lookat', 'up', 'fov'), prop_strs))
        camera_node = ET.SubElement(handle, 'Camera', prop_dict)

    def feed_api(self, scene):
        pos, look_at, up_vec = self.get_camera_infos()
        fov = self.get_fov() / math.pi * 180
        props = self.get_props()
        near_plane = getattr(props, 'near_plane', 1)
        far_plane = getattr(props, 'far_plane', 1000)
        scene.set_camera(pv.create_vec3f(pos.to_tuple()),\
            pv.create_vec3f(look_at.to_tuple()),\
            pv.create_vec3f(up_vec.to_tuple()),\
            near_plane, far_plane, fov)