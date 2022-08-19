import os
from . import config


# Sadly bl_info related fields cannot be put into config or it will coz an 
# ast parse traceback
bl_info = {
    "name": "bazen",
    "author": "Joey Chen",
    "version": (0, 0, 1),
    "blender": (3, 2, 0),
    "location": "",
    "description": "Blender Addon Template for Renderers",
    "warning": "",
    "category": "Render"
}

if "bpy" in locals():
    import importlib
    importlib.reload(ui)
else:
    import bpy


def register():
    print('registering the {} renderer'.format(config.engine_name))
    from .utils.registry import regular_registry, shading_node_registry, property_group_registry
    from . import render
    from . import ui
    render.setup()
    ui.setup()

    from . import nodes
    nodes.register()

    property_group_registry.register()
    regular_registry.register()
    shading_node_registry.register()


def unregister():
    from .utils.registry import regular_registry, shading_node_registry, property_group_registry
    from . import nodes
    nodes.unregister()

    property_group_registry.unregister()
    regular_registry.unregister()
    shading_node_registry.unregister()


if __name__ == '__main__':
    register()