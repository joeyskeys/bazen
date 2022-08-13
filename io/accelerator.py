
import bpy
import xml.etree.ElementTree as ET
from .base import BaseIO


class AcceleratorIO(BaseIO):
    """
    """

    def __init__(self):
        pass

    def get_props(self):
        return bpy.context.scene.bitto_accelerator_props

    def write_description(self, handle):
        props = self.get_props()
        acc_node = ET.SubElement(handle, props.accelerator_type)

    def feed_api(self):
        pass