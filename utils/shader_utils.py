
def get_light_shader_name(lgt):
    return lgt.name + '_shader'

def get_shader_from_material(mat):
    # Get output node from active material
    output_node = self.find_node(material.node_tree.nodes, node_name)

    if output_node is None:
        raise Exception('Cannot find output node for material : %s' %material.name)

    # Get shader node from output surface socket
    shader = output_node.inputs[socket_index].links[0].from_node
    
    return shader