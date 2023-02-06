import bpy


def pool_object(context):
    return context.object and not context.object.library