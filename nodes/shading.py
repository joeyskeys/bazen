from genericpath import isfile
import os
import bpy
from .. import config
from ..utils.registry import shading_node_registry, ShadingNode
from ..ui.preferences import get_pref
from ..utils.typemap import bprop_map, bsocket_map

from ..pyzen import osl


class BittoOSLNode(bpy.types.ShaderNode):
    """
    Base class for shading nodes
    """

    bl_idname = 'BittoOSLNode'    
    bl_label = 'OSL Material'
    bl_icon = 'NODE'
    
    node_type = 'osl'
    file_name = ''

    @classmethod
    def poll(cls, tree: bpy.types.NodeTree):
        return tree.bl_idname == 'bitto_material_nodes'
    
    def draw_buttons(self, context, layout):
        for input in self.inputs:
            pass

    def draw_buttons_ext(self, context, layout):
        pass

    def init(self, context):
        pass


def get_oso_info(oso_name, search_path):
    q = osl.Querier(oso_name, search_path)
    shader_info = {
        'name' : q.shadername(),
        'type' : q.shadertype(),
        'params' : []
    }

    param_infos = []
    for i in range(q.nparams()):
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
            param_infos.append(param_info)
    
    return (q.shadername(), q.shadertype(), param_infos)


def load_osl_shaders():
    shader_infos = {}
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    shader_folder_path = cur_dir + '/../shader'
    for shader_item in os.listdir(shader_folder_path):
        full_path = os.path.join(shader_folder_path, shader_item)
        if not os.path.isfile(full_path):
            continue
        if shader_item.endswith('.oso'):
            filename = shader_item.split('.')[0]
            oso_info = get_oso_info(filename, shader_folder_path)
            shader_infos[filename] = oso_info

    return shader_infos


def generate_shader_nodes():
    node_infos = load_osl_shaders()
    node_classes = []
    for node_name, node_info in node_infos.items():
        cap_name = node_name.capitalize()
        cap_cls_name = 'Bazen' + cap_name
        node_cls = type(cap_cls_name, (BittoOSLNode,), {})
        node_cls.bl_icon = 'MATERIAL'
        node_cls.bl_compatibility = {config.engine_name}
        node_cls.bl_label = cap_name
        node_cls.bl_idname = cap_cls_name 
        node_cls.node_name = node_name
        node_cls.__annotations__ = {}

        node_classes.append((node_cls, 'Material'))

    return node_classes


def setup():
    new_nodes = generate_shader_nodes()
    for node_cls, node_category in new_nodes:
        shading_node_registry.add_new_shading_class(node_cls, node_category)
