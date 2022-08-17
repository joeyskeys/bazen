
import os, subprocess

from nodes.shading import BittoOSLNode
from ..ui.preferences import get_pref


def get_oso_info(oslinfo, oso_path):
    oslinfo_cmd = ' '.join([oslinfo, oso_path])
    ret = subprocess.run(oslinfo_cmd, shell=True, stdout=subprocess.PIPE)
    return ret.stdout.decode('utf-8')


def parse_param_info(param_line):
    # Currently we don't have python binding to get the information of oso parameters,
    # use the osl utility for now
    comps = param_line.split(' ')
    ptype = comps[0]
    pname = comps[1]
    pdefault = None
    if ptype in ('color', 'point', 'vector', 'normal'):
        pdefault = map(float, comps[3 : 6])
    else:
        # This works only for basic types
        pdefault = eval('{}({})'.format(ptype, comps[2]))
    return (ptype, pname, pdefault)


def load_osl_shaders():
    perf = get_pref()
    osl_query_location = getattr(perf, 'osl_query_location', None)
    if not osl_query_location:
        raise Exception('osl query location not set')

    osl_shader_location = getattr(perf, 'osl_shader_location', None)
    if not osl_shader_location:
        raise Exception('osl shader location not set')

    shader_infos = {}
    if os.path.isdir(osl_shader_location):
        for shader in os.listdir(osl_shader_location):
            if shader.endswith('.oso'):
                param_infos = []
                info = get_oso_info(osl_query_location, os.path.join(osl_shader_location, shader))
                for param_line in info:
                     param_infos.append(parse_param_info(param_line))
                shader_infos[shader.split('.')[0]] = param_infos

    return shader_infos


def generate_shader_nodes():
    node_infos = load_osl_shaders()
    node_clss = []
    for node_name, node_info in node_infos.items():
        cap_name = node_name.capitalize()
        node_cls = type(cap_name, (BittoOSLNode), {})
        node_cls.bl_icon = 'MATERIAL'
        node_cls.bl_label = cap_name
        # Currently have no way to identify whether is shader node or a texture node
        # Output
        node_cls.outputs.new('NodeSocketColor', 'Color')

        # Inputs
        for input_info in node_info:
            input_socket = node_cls.inputs.new(input_info[0], input_info[1])
            input_socket.default_value = input_info[2]

        # Attributes
        # TODO : oslinfo cannot get metadata information

        node_clss.append((node_clss, 'Material'))

    return node_clss