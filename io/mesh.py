
import bpy
import xml.etree.ElementTree as ET
from .base import BaseIO


class MeshIO(BaseIO):
    """
    """

    def __init__(self):
        pass

    def write_description(self, handle, obj):
        obj.select_set(True)
        bpy.ops.export_scene.obj(filepath='meshes/{}.obj'.format(obj.name),
            check_existing=False, use_selection=True, use_triangles=True)
        mesh_props = {
            'filename' : 'string meshes/{}.obj'.format(obj.name),
            'shader_name' : obj.active_material.name
        }
        mesh_node = ET.SubElement(handle, 'Mesh', mesh_props)


    def feed_api(self):
        pass