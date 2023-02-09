import bpy
from .. import config


def poll_object(context):
    return context.object and not context.object.library


def poll_nodetree(tree_type):
    if config.use_seprate_node_editor:
        return tree_type == 'bitto_material_nodes'
    else:
        return tree_type == 'ShaderNodeTree'