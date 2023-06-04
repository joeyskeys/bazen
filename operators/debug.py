import typing
import bpy
from bpy.types import Context
from ..utils.registry import regular_registry, menu_registry


class DebugRenderOperator(bpy.types.Operator):
    bl_idname = 'bitto.debug_render'
    bl_label = 'Debug'
    bl_description = 'Invoke render process for a specific pixel'

    @classmethod
    def poll(cls, context):
        return True

    @staticmethod
    def find_window_region(space):
        for region in space.regions:
            if region.type == 'WINDOW':
                return region
        raise Exception('Cannot find window region')

    def execute(self, ctx):
        return {'FINISHED'}

    def modal(self, ctx, event):
        if event.type == 'MOUSEMOVE':
            pass
        elif event.type == 'LEFTMOUSE':
            region = self.find_window_region(ctx.area)
            u, v = region.view2d.region_to_view(event.mouse_region_x, event.mouse_region_y)
            if u < 0 or u > 1 or v < 0 or v > 1:
                print('clicked pixel out of image, cancelled')
                return {'CANCELLED'}

            # Very weird problem, the size for Render Result is 0, 0
            # Temporarily use render resolution, but notice this will introduce
            # another problem that the image size is not accurate
            # Imagine the user changed render resolution and run the operator
            # before he/she actually re-render the image
            # Perhaps we should explicitly set the image size after render
            # finished?(Confirmed, read-only property)
            #
            # Update: https://blender.stackexchange.com/questions/2170/how-to-access-render-result-pixels-from-python-script
            # This thread discusses the problem, answer by Iyad is viable but
            # it doesn't work during my test
            #
            #img_size = bpy.data.images['Render Result'].size
            #img_width = img_size[0]
            #img_height = img_size[1]

            img_width = ctx.scene.render.resolution_x
            img_height = ctx.scene.render.resolution_y
            pixel_x = int(u * img_width)
            pixel_y = int(v * img_height)

            # TODO: Invoke the debug render here...
            print('finished', pixel_x, pixel_y)
            return {'FINISHED'}
            
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            return {'CANCELLED'}
        
        return {'RUNNING_MODAL'}
    
    def invoke(self, ctx, event):
        wm = ctx.window_manager
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}
    

class IMAGE_MT_editor_debug(bpy.types.Menu):
    bl_label = "Debug"

    def draw(self, context):
        layout = self.layout
        layout.operator("bitto.debug_render", text="Debug Render")
    

def menu_func(self, ctx):
    layout = self.layout
    sima = ctx.space_data
    show_render = sima.show_render
    if show_render:
        layout.menu('IMAGE_MT_editor_debug')


def setup():
    regular_registry.add_new_class(DebugRenderOperator)
    regular_registry.add_new_class(IMAGE_MT_editor_debug)
    menu_registry.add_new_menu_func(bpy.types.IMAGE_MT_editor_menus, menu_func)