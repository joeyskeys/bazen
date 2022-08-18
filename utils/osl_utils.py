
from curses import meta
from importlib.metadata import metadata
import os, subprocess

from nodes.shading import BittoOSLNode
from ..ui.preferences import get_pref
from ..utils.typemap import bprop_map, bsocket_map


def get_oso_info(oslinfo, oso_path):
    oslinfo_cmd = ' '.join([oslinfo, '-v', oso_path])
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


def convert_param_value(ptype, pvalue_str):
    comps = pvalue_str.strip('[ ]').split(' ')
    val = None
    if ptype in ('color', 'point', 'vector', 'normal'):
        val = map(float, comps)
    elif ptype == 'string':
        val = pvalue_str
    else:
        val = eval('{}({})'.format(ptype, pvalue_str))

    return val


def parse_metadata(param_info):
    in_params = False
    param_name = None
    shader_info = { 'params' : [] }
    param_info = {}
    param_type = None
    for line in param_info:
        line = line.strip()
        if line.startswith('metadata:'):
            comps = line[len('metadata: ') :].split(' ')
            metatype = comps[0]
            metaname = comps[1]
            metavalue = comps[3]
            if in_params:
                param_info[metaname] = convert_param_value(metatype, metavalue)
            else:
                shader_info[metaname] = convert_param_value(metatype, metavalue)
        elif line.startswith('Default value: '):
            pvalue_str = line[len('Default value: ') :]
            param_info['default'] = convert_param_value(param_type, pvalue_str)
        elif line.startswith('surface') or line.startswith('volume') or line.startswith('displacement'):
            comps = line.split(' ')
            shader_info['type'] = comps[0]
            shader_info['name'] = comps[1].strip('"')
        else:
            if len(param_info) > 0:
                shader_info['params'].append(param_info)
                param_info = {}

            in_params = True
            comps = line.split(' ')
            param_info['name'] = comps[0].strip('"')
            param_type = comps[1].strip('"')
            param_info['type'] = param_type

    return shader_info


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
                shader_infos[shader.split('.')[0]] = parse_metadata(info)

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

        # Attributes
        # TODO : oslinfo cannot get metadata information

        node_clss.append((node_clss, 'Material'))

    return node_clss