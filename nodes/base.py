import bpy
from ..utils.polls import poll_nodetree


socket_type_map = {
    'int' : 'NodeSocketInt',
    'float' : 'NodeSocketFloat',
    'color' : 'NodeSocketColor',
    'normal' : 'NodeSocketVector',
    'string' : 'NodeSocketString',
}


class BittoNode(bpy.types.Node):
    """
    Base node class for bitto nodes
    """
    bl_icon = 'NODE'
    bl_label = ''

    @classmethod
    def poll(cls, tree):
        return poll_nodetree(tree.bl_idname)

    def draw_buttons(self, context, layout: 'UILayout'):
        pass

    def create_sockets_from_dict(self):
        print('calling create socket function for ', len(self.param_infos), ' params')
        for info in self.param_infos:
            socket_type = socket_type_map[info['type']]
            input_socket = self.inputs.new(socket_type, info['label'])
            input_socket.default_value = info['default']

    def init(self, context):
        self.create_sockets_from_dict()


class BittoShaderNode(BittoNode):
    def init(self, context):
        super(BittoShaderNode, self).init(context)
        self.outputs.new('NodeSocketShader', 'Output')


class BittoTextureNode(BittoNode):
    def init(self, context):
        super(BittoTextureNode, self).init(context)
        self.outputs.new('NodeSocketColor', 'Output')