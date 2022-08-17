
from . import nodetree
from . import shading


def register():
    nodetree.register()
    shading.setup()


def unregister():
    nodetree.unregister()