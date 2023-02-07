
from . import nodetree
from . import shading
from . import output


def setup():
    shading.setup()
    nodetree.setup()
    output.setup()