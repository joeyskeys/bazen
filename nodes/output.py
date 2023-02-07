import bpy
from .base import BittoNode
from ..utils.registry import regular_registry


class BittoNodeOutput(BittoNode):
    def init(self, context):
        self.inputs.new('NodeSocketShader', 'Surface')
        self.inputs.new('NodeSocketShader', 'Volume')
        self.inputs.new('NodeSocketShader', 'Displace')


def setup():
    regular_registry.add_new_class(BittoNodeOutput)