import os
import bpy
from ..nodes import shading
from .base import BaseIO
from ..utils.shader_utils import get_light_shader_name, get_shader_from_material, set_shader_param
from .. import pyzen


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

    def feed_api(self, scene, obj):
        # TODO : Maybe it's better to have to different methods..
        if obj.type == 'LIGHT':
            # This means it's a delta light
            node_name = 'ShaderNodeOutputLight'
            socket_index = 0
            # This's confusing, but light is difference from meshes
            # reconsider the TODO above 
            material = obj.data
            material_name = get_light_shader_name(obj)

            if material.node_tree is None:
                raise RuntimeError("Light {} doesn't have shader assigned".format(obj.name))
        else:
            node_name = 'ShaderNodeOutputMaterial'
            socket_index = 'Surface'
            material = obj.active_material
            material_name = material.name

        scene.begin_shader_group(material_name)

        shader = get_shader_from_material(material, node_name, socket_index)

        nodes = []
        connections = []
        params = {}

        def dfs(node):
            nodes.append(node)
            params[node] = []
            for input in node.inputs:
                if input.is_linked:
                    link = input.links[0]
                    # Recursive call to iterate through the tree
                    # TODO : change to a stack version if recursion is too slow
                    dfs(link.from_node)
                    # The connection follows the "from left to right" principle
                    # which means the 1st socket is the output of the upstream node
                    connections.append((link.from_socket, input))
                else:
                    params[node].append((node.param_infos[input.name]['name'], input.bl_idname, input.default_value))

        dfs(shader)

        lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../shader'))

        for node in nodes:
            param_vals = params[node]
            # The logic here follows the OSL API pattern
            # Setup the parameter value first and then load
            # the shader.
            for pv in param_vals:
                set_shader_param(scene, pv[0], pv[1], pv[2])
            scene.load_oso_shader('surface', node.node_name, node.name, lib_path)

        for src, dst in connections:
            scene.connect_shader(src.node.name, src.name, dst.node.name, dst.name)

        scene.end_shader_group()
