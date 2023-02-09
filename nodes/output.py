import bpy
from .base import BittoNode
from .. import config
from ..utils.registry import regular_registry


class BittoNodeOutput(BittoNode):
    bl_label = config.output_node_label

    def init(self, context):
        self.inputs.new('NodeSocketShader', 'Surface')
        self.inputs.new('NodeSocketShader', 'Volume')
        self.inputs.new('NodeSocketShader', 'Displace')


def setup():
    if config.use_seprate_node_editor:
        regular_registry.add_new_class(BittoNodeOutput)