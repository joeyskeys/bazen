
import os
from ..ui.preferences import get_pref


def load_osl_shaders():
    perf = get_pref()
    osl_query_location = getattr(perf, 'osl_query_location', None)
    if not osl_query_location:
        raise Exception('osl query location not set')

    osl_shader_location = getattr(perf, 'osl_shader_location', None)
    if not osl_shader_location:
        raise Exception('osl shader location not set')

    if os.path.isdir(osl_shader_location):
        for shader in os.listdir(osl_shader_location):
            if shader.endswith('.oso'):
                pass