
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