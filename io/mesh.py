
import bpy
import xml.etree.ElementTree as ET
from .base import BaseIO
from ..utils.obj_export import obj_export


class MeshIO(BaseIO):
    """
    """

    def __init__(self):
        pass

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
            'translate' : 'float3 {} {} {}'.format(translate.x, translate.z, -translate.y),
            'rotate' : 'float4 {} {} {} {}'.format(angle_axis[1], angle_axis[3], -angle_axis[2], angle_axis[0]),
            'scale' : 'float3 {} {} {}'.format(scale.x, scale.z, scale.y),
            'shader_name' : material_name
        }

        # Restore the rotation mode
        obj.rotation_mode = prev_mode

        mesh_node = ET.SubElement(handle, 'Mesh', mesh_props)

    def feed_api(self):
        pass