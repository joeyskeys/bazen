
import bpy
import nodeitems_utils
from .. import config
from ..utils.registry import regular_registry


class BittoNodeTree(bpy.types.NodeTree):
    """
    """

    bl_label = "Shader Editor"
    bl_idname = "bitto_material_nodes"
    bl_icon = "MATERIAL"

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == config.engine_name


def setup():
    regular_registry.add_new_class(BittoNodeTree)