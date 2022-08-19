
import bpy
import xml.etree.ElementTree as ET
from .base import BaseIO
from .mesh import MeshIO
from .material import MaterialIO
from .light import LightIO


class SceneIO(BaseIO):
    """
    """

    def __init__(self):
        self.meshio = MeshIO()
        self.materialio = MaterialIO()
        self.lightio = LightIO()

    def write_description(self, handle):
        self.lightio.write_description(handle)

        cur_selected = [o for o in bpy.context.scene.objects if o.select_get()]
        for obj in cur_selected:
            obj.select_set(False)

        objects_node = ET.SubElement(handle, 'Objects')
        for obj in bpy.context.scene.objects:
            if obj.hide_get():
                continue

            if obj.type == 'MESH':
                self.meshio.write_description(objects_node, obj)
                self.materialio.write_description(objects_node)
        
        for obj in cur_selected:
            obj.select_set(True)

    def feed_api(self):
        self.lightio.feed_api()
        
        for obj in bpy.context.scene.objects:
            if obj.hide_get():
                continue

            if obj.type == 'MESH':
                self.meshio.feed_api()
                self.materialio.feed_api()