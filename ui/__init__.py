from . import film
from . import camera
from . import integrator
from . import accelerator
from . import light
from . import material
from . import preferences
from . import sampler
from . import world
from . import node_editor


def setup():
    film.setup()
    camera.setup()
    integrator.setup()
    accelerator.setup()
    light.setup()
    material.setup()
    preferences.setup()
    sampler.setup()
    world.setup()