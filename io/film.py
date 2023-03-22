
import bpy
import mathutils
import xml.etree.ElementTree as ET
from .base import BaseIO


class FilmIO(BaseIO):
    """
    """

    def __init__(self):
        pass

    def get_resolution(self):
        render = bpy.context.scene.render
        return (render.resolution_x, render.resolution_y)

    def get_props(self):
        return bpy.context.scene.bitto_film_props

    def write_description(self, handle):
        prop_strs = list(map(' '.join, zip(['int'] * 2, list(map(str, self.get_resolution())))))
        prop_dict = dict(zip(('width', 'height'), prop_strs))
        film_node = ET.SubElement(handle, 'Film', prop_dict)

    def feed_api(self, scene):
        w, h = self.get_resolution()
        scene.set_film(w, h, output_path)