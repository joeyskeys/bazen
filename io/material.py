
import bpy
from ..nodes import shading
from .base import BaseIO


class MaterialIO(BaseIO):
    def __init__(self):
        pass

    def write_description(self, handle):
        '''
        def find_node(nodes, name):
            for n in nodes:
                if n.bl_idname == name:
                    return n
            return None

        # Get output node from active material
        material = meshobj.active_material
        output_node = find_node(material.node_tree.nodes, 'ShaderNodeOutputMaterial')

        if output_node is None:
            raise Exception('Cannot find output node for material : %s' % material.name)

        # Get shader node from output surface socket
        shader = output_node.inputs['Surface'].links[0].from_node
        # Do the actual writing
        if hasattr(shader, 'write_description'):
            shader.write_description(handle)
        else:
            # No shader fits
            print('None proper material assigned : %s' %shader.name)
            raise Exception('None proper material assigned : %s' %shader.name)
        '''
        pass

    def feed_api(self, scene):
        pass