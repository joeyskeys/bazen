from genericpath import isfile
import os
import bpy
from ..utils.registry import shading_node_registry, ShadingNode
from ..ui.preferences import get_pref
from ..utils.typemap import bprop_map, bsocket_map

import pyzen
from pyzen import osl


class BittoOSLNode(bpy.types.ShaderNode):
    """
    Base class for shading nodes
    """

    bl_idname = 'BittoOSLNode'    
    bl_label = 'OSL Material'
    bl_icon = 'NODE'
    
    node_type = 'osl'
    file_name = ''
    
    def draw_buttons(self, context, layout):
        for input in self.inputs:
            pass

    def draw_buttons_ext(self, context, layout):
        pass

    def init(self, context):
        pass


def get_oso_info(oso_name, search_path):
    #oslinfo_cmd = ' '.join([oslinfo, '-v', oso_path])
    #ret = subprocess.run(oslinfo_cmd, shell=True, stdout=subprocess.PIPE)
    #return ret.stdout.decode('utf-8')
    q = osl.Querier(oso_name, search_path)
    shader_info = {
        'name' : q.getshadername(),
        'type' : q.getshadertype(),
        'params' : []
    }

    for i in range(q.nparams()):
        '''
        baset = param.getparambasetype(i)
        dfts = None
        if baset in ('float', 'double'):
            dfts = q.getdefaultsf(i)
        elif baset in ('int', 'uint', 'int8', 'uint8', 'int16', 'uint16', 'int64', 'uint64'):
            dfts = q.getdefaultsi(i)
        else:
            dfts = q.getdefaultss(i)
        shader_info['params'].append((q.getparamname(i), q.getparamtype(i), dfts))
        '''

        param = q.getparam(i)
        param_info = {
            'name' : param.getname(),
            'type' : param.gettype(),
        }
        metadatas = param.getmetadatas()
        for metadata in metadatas:
            metatype = metadata.getbasetype()
            default = None
            if metatype == 'int':
                default = metadata.getdefaulti()
            elif metatype == 'float':
                default = metadata.getdefaultf()
            else:
                default = metadata.getdefaults()
            param_info[metadata.getname()] = default
    
    return (q.shadername(), q.shadertype(), param_infos)


def load_osl_shaders():
    '''
    perf = get_pref()
    osl_query_location = getattr(perf, 'osl_query_location', None)
    if not osl_query_location:
        print('osl query location not set')
        return {}

    osl_shader_location = getattr(perf, 'osl_shader_location', None)
    if not osl_shader_location:
        print('osl shader location not set')
        return {}
    '''

    shader_infos = {}
    shader_folder_path = './shader'
    for shader_item in os.listdir(shader_folder_path):
        full_path = os.path.join(shader_folder_path, shader_item)
        if not os.isfile(full_path):
            continue
        if shader_item.endswith('.oso'):
            filename = shader_item.split('.')[0]
            oso_info = get_oso_info(filename, shader_folder_path)
            shader_infos[filename] = oso_info

    return shader_infos


def generate_shader_nodes():
    node_infos = load_osl_shaders()
    node_clss = []
    for node_name, node_info in node_infos.items():
        cap_name = node_name.capitalize()
        node_cls = type(cap_name, (BittoOSLNode), {})
        node_cls.bl_icon = 'MATERIAL'
        node_cls.bl_label = cap_name
        node_cls.__annotations__ = {}
        # Currently have no way to identify whether is shader node or a texture node
        # Output
        node_cls.outputs.new('NodeSocketColor', 'Color')

        # Inputs
        for input_info in node_info['params']:
            if input_info['connectable']:
                input_socket = node_cls.inputs.new(
                    bsocket_map[input_info['type']], input_info['name'])
                input_socket.default_value = input_info['default']
            else:
                node_cls.__annotations__[input_info['name']] = bprop_map[input_info['type']](
                    name=input_info['name'], default=input_info['default'])

        node_clss.append((node_clss, 'Material'))

    return node_clss


def setup():
    new_nodes = generate_shader_nodes()
    for node_cls, node_category in new_nodes:
        shading_node_registry.add_new_shading_class(node_cls, node_category)
