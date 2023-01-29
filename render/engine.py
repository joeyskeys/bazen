
import os
import bpy
import threading
import time
import pyzen
from .tile_callback import TileCallback
from .. import config
from ..io.output import BittoOutput
from ..ui.preferences import get_pref
from ..utils.registry import regular_registry


class BittoRenderThread(threading.Thread):
    def __init__(self, renderer):
        super(BittoRenderThread, self).__init__()
        self.renderer = renderer

    def run(self):
        self.renderer.render()


class BittoRenderEngine(bpy.types.RenderEngine):
    bl_idname = config.engine_name
    bl_label = config.engine_label
    bl_use_preview = True
    bl_use_shading_nodes = False
    bl_use_postprocess = True

    # Ctor
    def __init__(self):
        self.renderer = None
        self.tile_cbk = None
        self.render_thread = None

    def __del__(self):
        pass

    def render(self, depsgraph):
        #output = BittoOutput()
        #output.write_description('D:/tmp')

        self.tile_cbk = TileCallback(self)

        pref = get_pref()
        sample_cnt = getattr(pref, 'sample_cnt', 5)
        thread_cnt = getattr(pref, 'thread_cnt', os.cpu_count())
        self.renderer = pyzen.api.Renderer(sample_cnt, thread_cnt, self.tile_cbk)

        self.render_thread = BittoRenderThread(self.renderer)
        self.render_thread.start()
        while self.render_thread.isAlive():
            self.render_thread.join(0.5)

        self._cleanup()

    def view_update(self, context, depsgraph):
        pass

    def view_draw(self, context, depsgraph):
        pass

    def _cleanup(self):
        # Need to stop the running thread first..
        self.render_thread = None
        self.renderer = None
        self.tile_cbk = None


def setup():
    regular_registry.add_new_class(BittoRenderEngine)