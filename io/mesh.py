
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

        mesh_props = {
            'filename' : 'string meshes/{}.obj'.format(obj.name),
            'shader_name' : material_name
        }
        mesh_node = ET.SubElement(handle, 'Mesh', mesh_props)


    def feed_api(self):
        pass