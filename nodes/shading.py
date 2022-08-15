
import bpy
from ..utils.registry import shading_node_registry, ShadingNode
from ..utils.osl_utils import load_osl_shaders


class BittoOSLNode(bpy.types.ShaderNode):
    """
    Base class for shading nodes
    """

    bl_idname = 'BittoOSLNode'    
    bl_label = 'OSL Material'
    bl_icon = 'NODE'
    
    node_type = 'osl'
    file_name = ''
    
    def draw_buttons(self, context, layout):
        for input in self.inputs:
            pass

    def draw_buttons_ext(self, context, layout):
        pass

    def init(self, context):
        pass