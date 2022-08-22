
from .camera import CameraIO
from .film import FilmIO
from .sampler import SamplerIO
from .integrator import IntegratorIO
from .accelerator import AcceleratorIO
from .scene import SceneIO
from ..ui import preferences
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os


class BittoOutput(object):
    """
    """

    def __init__(self):
        self.cameraio = CameraIO()
        self.filmio = FilmIO()
        self.samplerio = SamplerIO()
        self.integratorio = IntegratorIO()
        self.acceleratorio = AcceleratorIO()
        self.sceneio = SceneIO()
        
    def write_description(self, path):
        #root = ET.fromstring('<Scene/>')
        scene_node = ET.Element('Scene')
        tree = ET.ElementTree(scene_node)

        self.filmio.write_description(scene_node)
        self.cameraio.write_description(scene_node)
        self.samplerio.write_description(scene_node)
        self.integratorio.write_description(scene_node)
        self.acceleratorio.write_description(scene_node)
        self.sceneio.write_description(scene_node, path)

        #tree.write(path)
        raw = ET.tostring(scene_node, encoding='utf-8')
        pretty = minidom.parseString(raw).toprettyxml(indent='  ')
        filename = os.path.join(path, 'output.xml')
        with open(filename, 'w') as f:
            f.write(pretty)


    def feed_api(self):
        self.filmio.feed_api()
        self.cameraio.feed_api()
        self.samplerio.feed_api()
        self.integratorio.feed_api()
        self.acceleratorio.feed_api()
        self.sceneio.feed_api()