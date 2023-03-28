
import bpy
from ..nodes import shading
from .base import BaseIO
from .. import pyzen


class MaterialIO(BaseIO):
    def __init__(self):
        pass

    @staticmethod
    def find_node(nodes, name):
        for n in nodes:
            if n.bl_idname == name:
                return n
        return None

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

    def feed_api(self, scene, obj):
        # Get output node from active material
        material = obj.active_material
        output_node = self.find_node(material.nodetree.nodes, 'ShaderNodeOutputMaterial')

        if output_node is None:
            raise Exception('Cannot find output node for material : %s' %material.name)

        pyzen.api.begin_shader_group(material.name)

        # Get shader node from output surface socket
        shader = output_node.inputs['Surface'].links[0].from_node

        nodes = []
        connections = []

        def dfs(node):
            nodes.append(node)
            for input in self.inputs:
                if input.is_linked:
                    link = input.links[0]
                    # Recursive call to iterate through the tree
                    # TODO : change to a stack version if recursion is too slow
                    dfs(link.from_node)
                    # The connection follows the "from left to right" principle
                    # which means the 1st socket is the output of the upstream node
                    connections.append((link.from_socket, input))

        dfs(shader)

        for node in nodes:
            pyzen.api.load_oso_shader('surface', node.node_name, node.name)
        for src, dst in connections:
            pyzen.api.connect_shader(src.node.name, src.name, dst.node.name, dst.name)

        pyzen.api.end_shader_group()
