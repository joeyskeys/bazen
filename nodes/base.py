import bpy


class BittoNode(bpy.types.Node):
    """
    Base node class for bitto nodes
    """
    bl_label = ''

    @classmethod
    def poll(cls, tree):
        return tree.bl_idname == 'bitto_material_nodes'

    def init(self, context):
        self.outputs.new('NodeSocketShader', 'Output')

    def draw_buttons(self, context, layout: 'UILayout'):
        pass
