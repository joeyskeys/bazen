import os, sys
from . import config
from .utils.registry import *


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
    regular_registry.cleanup()
    shading_node_registry.cleanup()
    property_group_registry.cleanup()
    menu_registry.cleanup()

    from . import render
    from . import ui
    from . import operators
    from . import nodes
    render.setup()
    ui.setup()
    # node_editor register is a little bit different which is just a function replacement
    ui.node_editor.register()
    operators.setup()
    nodes.setup()

    property_group_registry.register()
    regular_registry.register()
    shading_node_registry.register()
    menu_registry.register()

    from .nodes import category
    category.register()


def unregister():
    menu_registry.unregister()
    property_group_registry.unregister()
    regular_registry.unregister()
    shading_node_registry.unregister()

    from . import ui
    ui.node_editor.unregister()

    from .nodes import category
    category.unregister()


if __name__ == '__main__':
    register()