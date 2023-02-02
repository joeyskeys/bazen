
import bpy
from bl_ui.properties_material import MATERIAL_PT_viewport
from .. import config
from .base import BittoProperties, setup_ui
from ..utils.registry import regular_registry, property_group_registry


#original_viewport_draw = None


#def bitto_mat_template_ID(layout, material):
    #row = layout.row(align=True)


class BITTO_PT_materialslots(bpy.types.Panel):
    bl_label = "Material"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"

    @classmethod
    def poll(cls, context):
        renderer = context.scene.render
        return (context.material or context.object) and renderer.engine == config.engine_name

    def draw(self, context):
        layout = self.layout
        mat = context.material
        slot = context.material_slot
        obj = context.object
        space = context.space_data


class BITTO_PT_materialdetails(bpy.types.Panel):
    bl_label = "Details"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"

    @classmethod
    def poll(cls, context):
        #renderer = context.scene.render
        #return (context.material or context.object) and renderer.engine == config.engine_name
        mat = context.object.active_material is not None
        if mat:
            renderer = context.scene.render.engine == config.engine_name
            obj = context.object is not None
            obj_type = context.object.type == 'MESH'
            return renderer and obj and obj_type
        return False

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        obj = context.object
        mat = obj.active_material
        

        #material_props = context.scene.


def setup():
    regular_registry.add_new_class(BITTO_PT_materialslots)
