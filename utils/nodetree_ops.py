import bpy


def init_nodetree(nt):
    nt.use_fake_user = True

    nodes = nt.nodes

    output = nodes.new('BittoNodeOutput')
    output.location = 300, 200
    output.select = False

    # Create a default material here
    #disney = nodes.new()
    #disney.location = 50, 200

    #nt.links.new(disney.outputs[0], output.inputs[0])


def show_nodetree(ctx, nt):
    for area in ctx.screen.areas:
        if area.type = 'NODE_EDITOR':
            for space in area.spaces:
                if space.type == 'NODE_EDITOR' and not space.pin:
                    space.tree_type = nt.bl_idname
                    space.node_tree = nt
                    return True
    return False