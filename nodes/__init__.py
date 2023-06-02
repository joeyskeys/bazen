
from . import nodetree
from . import shading
from . import output
from . import category


def setup():
    shading.setup()
    nodetree.setup()
    output.setup()