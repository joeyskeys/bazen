
import bpy
from .. import config
from .base import BittoProperties
from ..utils.registry import regular_registry, property_group_registry


class BittoWorldProperties(BittoProperties):
    pass

BittoWorldProperties.init_annotations(config.world_props)


class Bitto_PT_world(bpy.types.Panel):
    bl_label = "World"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    COMPAT_ENGINES = {config.engine_name}
    bl_context = "world"

    @classmethod
    def poll(cls, context):
        renderer = context.scene.render
        return render.engine == config.engine_name

    def draw(cls, context):
        layout = self.layout
        layout.use_property_split = True

        world_props = context.scene.bitto_world_props
        setup_ui(layout, config.world_props, world_props)


def setup():
    regular_registry.add_new_class(Bitto_PT_world)
    property_group_registry.add_new_property_class(BittoWorldProperties, bpy.types.Scene, "bitto_world_props")