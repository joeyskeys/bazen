
import bpy
import mathutils
import xml.etree.ElementTree as ET
from .base import BaseIO
import pyzen


class IntegratorIO(BaseIO):
    """
    """

    def __init__(self):
        pass

    def get_props(self):
        return bpy.context.scene.bitto_integrator_props

    def write_description(self, handle):
        props = self.get_props()
        integrator_node = ET.SubElement(handle, props.integrator_type)

    def feed_api(self, scene):
        props = self.get_props()
        integrator_type_str = getattr(props, 'integrator_type', 'PathIntegrator')
        integrator_type = getattr(pyzen.api.IntegratorType, integrator_type_str,\
            pyzen.api.IntegratorType.PathIntegrator)
        scene.set_integrator(integrator_type)