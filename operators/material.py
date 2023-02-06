import bpy
from ..utils import polls
from ..utils import nodetree_ops as ntop
from ..utils.registry import regular_registry


class BITTO_OT_material_new(bpy.types.Operator):
    bl_idname = 'bitto.material_new'
    bl_label = 'New'
    bl_description = 'Create a new material and node tree'
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return polls.poll_object(context)

    def execute(self, context):
        mat = bpy.data.materials.new(name='Material')
        tree_name = 'Nodes_' + mat.name
        nodetree = bpy.data.node_groups.new(name=tree_name, type='bitto_material_nodes')
        ntop.init_nodetree(nodetree)
        mat.bitto_nodetree = nodetree

        obj = context.active_object
        if obj.material_slots:
            obj.material_slots[obj.active_material_index].material = mat
        else:
            obj.data.materials.append(mat)

        obj.update_tag()
        ntop.show_nodetree(context, nodetree)

        return {'FINISHED'}


def setup():
    regular_registry.add_new_class(BITTO_OT_material_new)