
import bpy
import nodeitems_utils
from .. import config
from ..utils.registry import regular_registry


class BittoNodeTree(bpy.types.NodeTree):
    """
    """

    bl_label = config.node_editor_name
    bl_idname = "bitto_material_nodes"
    bl_icon = "MATERIAL"

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == config.engine_name


def setup():
    regular_registry.add_new_class(BittoNodeTree)