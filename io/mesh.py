
import bpy
import xml.etree.ElementTree as ET
from .base import BaseIO
from ..utils.obj_export import obj_export
from ..utils import triangulate as tr


class MeshIO(BaseIO):
    """
    """

    def __init__(self):
        pass

    def get_mesh_infos(self, obj):
        translation = tuple(obj.location)

        prev_rot_mode = obj.rotation_mode
        obj.rotation_mode = 'AXIS_ANGLE'
        angle_axis = tuple(obj.rotation_axis_angle)
        obj.rotation_mode = prev_rot_mode

        scale = tuple(obj.scale)

        if obj.active_material is None:
            material_name = 'Error'
        else:
            material_name = obj.active_material.name

    def write_description(self, handle, obj, path):
        obj_export(obj, path)
        if obj.active_material is None:
            material_name = 'Error'
        else:
            material_name = obj.active_material.name

        translate = obj.location
        prev_mode = obj.rotation_mode
        obj.rotation_mode = 'AXIS_ANGLE'
        angle_axis = obj.rotation_axis_angle
        scale = obj.scale

        mesh_props = {
            'filename' : 'string meshes/{}.obj'.format(obj.name),
            'shader_name' : material_name
        }

        if abs(translate.x) + abs(translate.y) + abs(translate.z) > 1e-6:
            mesh_props.update({'translate' : 'float3 {} {} {}'.format(translate.x, translate.z, -translate.y)})
        if abs(angle_axis[0]) > 1e-6:
            mesh_props.update({'rotate' : 'float4 {} {} {} {}'.format(angle_axis[1], angle_axis[3], -angle_axis[2], angle_axis[0])})
        if abs(scale.x - 1) + abs(scale.y - 1) + abs(scale.z - 1) > 1e-6:
            mesh_props.update({'scale' : 'float3 {} {} {}'.format(scale.x, scale.z, scale.y)})

        # Restore the rotation mode
        obj.rotation_mode = prev_mode

        mesh_node = ET.SubElement(handle, 'Mesh', mesh_props)

    def feed_api(self, scene, obj):
        pass