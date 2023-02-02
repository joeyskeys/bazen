
import bpy
import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem
from nodeitems_builtins import ShaderNodeCategory
from .. import config
from ..utils.registry import shading_node_registry


class BittoNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == config.engine_name \
            and context.space_data.tree_type == 'bitto_material_nodes'


'''
original_poll_func = None

def hide_func(cls, context):
    return context.scene.render.engine != config.engine_name
'''


def register():
    #global original_poll_func
    #original_poll_func = ShaderNodeCategory.poll
    #ShaderNodeCategory.poll = hide_func

    bitto_shader_node_categories = []
    for category, label in config.node_categories:
        print('creating category : ', category, label)
        bitto_shader_node_categories.append(BittoNodeCategory(category, label, items=
            [NodeItem(node_info[0]) for node_info in shading_node_registry.node_categories[label]]))
    nodeitems_utils.register_node_categories(config.category_name, bitto_shader_node_categories)


def unregister():
    #ShaderNodeCategory.poll = original_poll_func
    nodeitems_utils.unregister_node_categories(config.category_name)