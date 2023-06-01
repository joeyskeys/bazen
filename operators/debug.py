import typing
import bpy
from bpy.types import Context
from ..utils.registry import regular_registry, menu_registry


class DebugRenderOperator(bpy.types.Operator):
    bl_idname = 'bitto.debug_render'
    bl_label = 'Debug'
    bl_description = 'Invoke render process for a specific pixel'
    bl_options = {}

    mouse_x: bpy.props.IntProperty(name="Mouse X Coordinate")
    mouse_y: bpy.props.IntProperty(name="Mouse Y Coordinate")

    @classmethod
    def poll(cls, context):
        return True
    
    def invoke(self, ctx, event):
        self.x = event.mouse_x
        self.y = event.mouse_y
        wm = ctx.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, ctx):
        self.report({'INFO'}, 'input {}, {}, move {}, {}'.format(self.mouse_x, self.mouse_y, self.x, self.y))
        return {'FINISHED'}
    

class IMAGE_MT_editor_debug(bpy.types.Menu):
    bl_label = "Debug"

    def draw(self, context):
        layout = self.layout
        layout.operator("bitto.debug_render", text="Debug Render")
    

def menu_func(self, ctx):
    layout = self.layout
    layout.menu('IMAGE_MT_editor_debug')


def setup():
    regular_registry.add_new_class(DebugRenderOperator)
    regular_registry.add_new_class(IMAGE_MT_editor_debug)
    menu_registry.add_new_menu_func(bpy.types.IMAGE_MT_editor_menus, menu_func)