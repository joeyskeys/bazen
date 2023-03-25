
import bpy
from .base import BaseIO
import pyzen.vec as pzvec


class LightIO(BaseIO):
    """
    """

    def __init__(self):
        pass

    def get_props(self):
        return object.data.bitto_light_props

    def write_description(self, handle):
        pass

    def feed_api(self, scene, obj):
        light_type = obj.data.type
        light_color = obj.data.color.to_tuple()
        light_loc = obj.location.to_tuple()

        if light_type == 'POINT':
            scene.add_point_light(pzvec.Vec3f(*light_color), pzvec.Vec3f(*light_loc))
        else:
            print('Type {} of {} is not supported yet'.format(light_type, obj.name))