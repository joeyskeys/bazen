from ..pyzen import vec as pv

def get_light_shader_name(lgt):
    return lgt.name + '_shader'

def find_node(nodes, name):
    for n in nodes:
        if n.bl_idname == name:
            return n
    return None

def get_shader_from_material(mat, node_name, socket_index):
    # Get output node from active material
    output_node = find_node(mat.node_tree.nodes, node_name)

    if output_node is None:
        raise Exception('Cannot find output node for material : {}'.format(mat.name))

    # Get shader node from output surface socket
    shader = output_node.inputs[socket_index].links[0].from_node
    
    return shader

def set_shader_param(scene, pname, ptype, pvalue):
    if ptype == 'NodeSocketColor' or ptype == 'NodeSocketVector':
        scene.set_shader_param_vec3f(pname, pv.Vec3f(pvalue[0], pvalue[1], pvalue[2]))
    elif ptype == 'NodeSocketFloat':
        scene.set_shader_param_float(pname, float(pvalue))
    else:
        raise Exception('Socket type {} not supported'.format(ptype))