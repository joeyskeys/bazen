from bl_ui.space_node import NODE_HT_header, NODE_MT_editor_menus
from .material import bitto_mat_template_ID
from .. import config
from ..utils.polls import poll_nodetree

original_draw = None


# Most part of this function is copied from bl_ui/space_node.py
# Add a branch for snode.tree_type == 'bitto_material_nodes' to
# add custom node_editor header
def custom_node_header_draw(panel, context):
    layout = panel.layout

    scene = context.scene
    snode = context.space_data
    overlay = snode.overlay
    snode_id = snode.id
    id_from = snode.id_from
    tool_settings = context.tool_settings
    is_compositor = snode.tree_type == 'CompositorNodeTree'

    layout.template_header()

    # Now expanded via the `ui_type`.
    # layout.prop(snode, "tree_type", text="")
    
    types_that_support_material = {'MESH', 'CURVE', 'SURFACE', 'FONT', 'META',
                                    'GPENCIL', 'VOLUME', 'CURVES', 'POINTCLOUD'}

    if snode.tree_type == 'ShaderNodeTree':
        layout.prop(snode, "shader_type", text="")

        ob = context.object
        if snode.shader_type == 'OBJECT' and ob:
            ob_type = ob.type

            NODE_MT_editor_menus.draw_collapsible(context, layout)

            # No shader nodes for Eevee lights
            if snode_id and not (context.engine == 'BLENDER_EEVEE' and ob_type == 'LIGHT'):
                row = layout.row()
                row.prop(snode_id, "use_nodes")

            layout.separator_spacer()

            # disable material slot buttons when pinned, cannot find correct slot within id_from (T36589)
            # disable also when the selected object does not support materials
            has_material_slots = not snode.pin and ob_type in types_that_support_material

            if ob_type != 'LIGHT':
                row = layout.row()
                row.enabled = has_material_slots
                row.ui_units_x = 4
                row.popover(panel="NODE_PT_material_slots")

            row = layout.row()
            row.enabled = has_material_slots

            # Show material.new when no active ID/slot exists
            if not id_from and ob_type in types_that_support_material:
                row.template_ID(ob, "active_material", new="material.new")
            # Material ID, but not for Lights
            if id_from and ob_type != 'LIGHT':
                row.template_ID(id_from, "active_material", new="material.new")

        if snode.shader_type == 'WORLD':
            NODE_MT_editor_menus.draw_collapsible(context, layout)

            if snode_id:
                row = layout.row()
                row.prop(snode_id, "use_nodes")

            layout.separator_spacer()

            row = layout.row()
            row.enabled = not snode.pin
            row.template_ID(scene, "world", new="world.new")

        if snode.shader_type == 'LINESTYLE':
            view_layer = context.view_layer
            lineset = view_layer.freestyle_settings.linesets.active

            if lineset is not None:
                NODE_MT_editor_menus.draw_collapsible(context, layout)

                if snode_id:
                    row = layout.row()
                    row.prop(snode_id, "use_nodes")

                layout.separator_spacer()

                row = layout.row()
                row.enabled = not snode.pin
                row.template_ID(lineset, "linestyle", new="scene.freestyle_linestyle_new")

    elif snode.tree_type == 'TextureNodeTree':
        layout.prop(snode, "texture_type", text="")

        NODE_MT_editor_menus.draw_collapsible(context, layout)

        if snode_id:
            layout.prop(snode_id, "use_nodes")

        layout.separator_spacer()

        if id_from:
            if snode.texture_type == 'BRUSH':
                layout.template_ID(id_from, "texture", new="texture.new")
            else:
                layout.template_ID(id_from, "active_texture", new="texture.new")

    elif snode.tree_type == 'CompositorNodeTree':

        NODE_MT_editor_menus.draw_collapsible(context, layout)

        if snode_id:
            layout.prop(snode_id, "use_nodes")

    elif snode.tree_type == 'GeometryNodeTree':
        NODE_MT_editor_menus.draw_collapsible(context, layout)
        layout.separator_spacer()

        ob = context.object

        row = layout.row()
        if snode.pin:
            row.enabled = False
            row.template_ID(snode, "node_tree", new="node.new_geometry_node_group_assign")
        elif ob:
            active_modifier = ob.modifiers.active
            if active_modifier and active_modifier.type == 'NODES':
                if active_modifier.node_group:
                    row.template_ID(active_modifier, "node_group", new="object.geometry_node_tree_copy_assign")
                else:
                    row.template_ID(active_modifier, "node_group", new="node.new_geometry_node_group_assign")
            else:
                row.template_ID(snode, "node_tree", new="node.new_geometry_nodes_modifier")

    ###############################################################################
    # Specialized node editor header code, this part is mostly copied from
    # https://github.com/LuxCoreRender/BlendLuxCore/blob/master/ui/node_editor.py
    # as well as the custom node editor idea
    elif snode.tree_type == 'bitto_material_nodes':
        NODE_MT_editor_menus.draw_collapsible(context, layout)

        ob = context.object

        if ob:
            layout.separator_spacer()
            ob_type = ob.type

            has_material_slots = not snode.pin and ob_type in types_that_support_material

            row = layout.row()
            row.enabled = has_material_slots
            row.ui_units_x = 4
            row.popover(panel='NODE_PT_material_slots')

            row = layout.row()
            row.enabled = has_material_slots

            mat = id_from if id_from else ob.active_material
            # bitto_mat_template_ID(row, mat)

            if mat and not mat.get('bitto_nodetree'):
                layout.operator('bitto.material_new', icon='NODETREE', text=config.node_editor_convert_text)
    ###############################################################################

    else:
        # Custom node tree is edited as independent ID block
        NODE_MT_editor_menus.draw_collapsible(context, layout)

        layout.separator_spacer()

        layout.template_ID(snode, "node_tree", new="node.new_node_tree")

    # Put pin next to ID block
    if not is_compositor:
        layout.prop(snode, "pin", text="", emboss=False)

    layout.separator_spacer()

    # Put pin on the right for Compositing
    if is_compositor:
        layout.prop(snode, "pin", text="", emboss=False)

    layout.operator("node.tree_path_parent", text="", icon='FILE_PARENT')

    # Backdrop
    if is_compositor:
        row = layout.row(align=True)
        row.prop(snode, "show_backdrop", toggle=True)
        sub = row.row(align=True)
        sub.active = snode.show_backdrop
        sub.prop(snode, "backdrop_channels", icon_only=True, text="", expand=True)

    # Snap
    row = layout.row(align=True)
    row.prop(tool_settings, "use_snap_node", text="")
    row.prop(tool_settings, "snap_node_element", icon_only=True)
    if tool_settings.snap_node_element != 'GRID':
        row.prop(tool_settings, "snap_target", text="")

    # Overlay toggle & popover
    row = layout.row(align=True)
    row.prop(overlay, "show_overlays", icon='OVERLAY', text="")
    sub = row.row(align=True)
    sub.active = overlay.show_overlays
    sub.popover(panel="NODE_PT_overlay", text="")


def modified_node_header_draw(panel, context):
    layout = panel.layout

    scene = context.scene
    snode = context.space_data
    overlay = snode.overlay
    snode_id = snode.id
    id_from = snode.id_from
    tool_settings = context.tool_settings
    is_compositor = snode.tree_type == 'CompositorNodeTree'

    layout.template_header()

    # Now expanded via the `ui_type`.
    # layout.prop(snode, "tree_type", text="")
    
    types_that_support_material = {'MESH', 'CURVE', 'SURFACE', 'FONT', 'META',
                                    'GPENCIL', 'VOLUME', 'CURVES', 'POINTCLOUD'}

    if snode.tree_type == 'ShaderNodeTree':
        layout.prop(snode, "shader_type", text="")

        ob = context.object
        if snode.shader_type == 'OBJECT' and ob:
            ob_type = ob.type

            NODE_MT_editor_menus.draw_collapsible(context, layout)

            # No shader nodes for Eevee lights
            if snode_id and not (context.engine == 'BLENDER_EEVEE' and ob_type == 'LIGHT'):
                row = layout.row()
                row.prop(snode_id, "use_nodes")

            layout.separator_spacer()

            # disable material slot buttons when pinned, cannot find correct slot within id_from (T36589)
            # disable also when the selected object does not support materials
            has_material_slots = not snode.pin and ob_type in types_that_support_material

            if ob_type != 'LIGHT':
                row = layout.row()
                row.enabled = has_material_slots
                row.ui_units_x = 4
                row.popover(panel="NODE_PT_material_slots")

            row = layout.row()
            row.enabled = has_material_slots

            # Show material.new when no active ID/slot exists
            if not id_from and ob_type in types_that_support_material:
                row.template_ID(ob, "active_material", new="material.new")
            # Material ID, but not for Lights
            if id_from and ob_type != 'LIGHT':
                row.template_ID(id_from, "active_material", new="material.new")

            layout.operator('bitto.material_convert', icon='NODETREE', text=config.node_editor_convert_text)
            layout.operator('bitto.material_recover', icon='NODETREE', text=config.node_editor_recover_text)

        if snode.shader_type == 'WORLD':
            NODE_MT_editor_menus.draw_collapsible(context, layout)

            if snode_id:
                row = layout.row()
                row.prop(snode_id, "use_nodes")

            layout.separator_spacer()

            row = layout.row()
            row.enabled = not snode.pin
            row.template_ID(scene, "world", new="world.new")

        if snode.shader_type == 'LINESTYLE':
            view_layer = context.view_layer
            lineset = view_layer.freestyle_settings.linesets.active

            if lineset is not None:
                NODE_MT_editor_menus.draw_collapsible(context, layout)

                if snode_id:
                    row = layout.row()
                    row.prop(snode_id, "use_nodes")

                layout.separator_spacer()

                row = layout.row()
                row.enabled = not snode.pin
                row.template_ID(lineset, "linestyle", new="scene.freestyle_linestyle_new")

    elif snode.tree_type == 'TextureNodeTree':
        layout.prop(snode, "texture_type", text="")

        NODE_MT_editor_menus.draw_collapsible(context, layout)

        if snode_id:
            layout.prop(snode_id, "use_nodes")

        layout.separator_spacer()

        if id_from:
            if snode.texture_type == 'BRUSH':
                layout.template_ID(id_from, "texture", new="texture.new")
            else:
                layout.template_ID(id_from, "active_texture", new="texture.new")

    elif snode.tree_type == 'CompositorNodeTree':

        NODE_MT_editor_menus.draw_collapsible(context, layout)

        if snode_id:
            layout.prop(snode_id, "use_nodes")

    elif snode.tree_type == 'GeometryNodeTree':
        NODE_MT_editor_menus.draw_collapsible(context, layout)
        layout.separator_spacer()

        ob = context.object

        row = layout.row()
        if snode.pin:
            row.enabled = False
            row.template_ID(snode, "node_tree", new="node.new_geometry_node_group_assign")
        elif ob:
            active_modifier = ob.modifiers.active
            if active_modifier and active_modifier.type == 'NODES':
                if active_modifier.node_group:
                    row.template_ID(active_modifier, "node_group", new="object.geometry_node_tree_copy_assign")
                else:
                    row.template_ID(active_modifier, "node_group", new="node.new_geometry_node_group_assign")
            else:
                row.template_ID(snode, "node_tree", new="node.new_geometry_nodes_modifier")


    else:
        # Custom node tree is edited as independent ID block
        NODE_MT_editor_menus.draw_collapsible(context, layout)

        layout.separator_spacer()

        layout.template_ID(snode, "node_tree", new="node.new_node_tree")

    # Put pin next to ID block
    if not is_compositor:
        layout.prop(snode, "pin", text="", emboss=False)

    layout.separator_spacer()

    # Put pin on the right for Compositing
    if is_compositor:
        layout.prop(snode, "pin", text="", emboss=False)

    layout.operator("node.tree_path_parent", text="", icon='FILE_PARENT')

    # Backdrop
    if is_compositor:
        row = layout.row(align=True)
        row.prop(snode, "show_backdrop", toggle=True)
        sub = row.row(align=True)
        sub.active = snode.show_backdrop
        sub.prop(snode, "backdrop_channels", icon_only=True, text="", expand=True)

    # Snap
    row = layout.row(align=True)
    row.prop(tool_settings, "use_snap_node", text="")
    row.prop(tool_settings, "snap_node_element", icon_only=True)
    if tool_settings.snap_node_element != 'GRID':
        row.prop(tool_settings, "snap_target", text="")

    # Overlay toggle & popover
    row = layout.row(align=True)
    row.prop(overlay, "show_overlays", icon='OVERLAY', text="")
    sub = row.row(align=True)
    sub.active = overlay.show_overlays
    sub.popover(panel="NODE_PT_overlay", text="")

def bitto_draw_switch(panel, context):
    if context.scene.render.engine == config.engine_name and \
        poll_nodetree(context.space_data.tree_type):
        if config.use_seprate_node_editor:
            custom_node_header_draw(panel, context)
        else:
            modified_node_header_draw(panel, context)
    else:
        original_draw(panel, context)


def register():
    global original_draw
    original_draw = NODE_HT_header.draw
    NODE_HT_header.draw = bitto_draw_switch


def unregister():
    NODE_HT_header = original_draw
