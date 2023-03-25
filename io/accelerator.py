
import bpy
import xml.etree.ElementTree as ET
from .base import BaseIO
from .. import pyzen


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

    def feed_api(self, scene):
        props = self.get_props()
        accelerator_type_str = getattr(props, 'accelerator_type', 'Embree')
        accelerator_type = getattr(pyzen.api.AcceleratorType, accelerator_type_str,\
            pyzen.api.AcceleratorType.Embree)
        scene.set_accelerator(accelerator_type)