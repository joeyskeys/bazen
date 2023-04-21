import logging
from .. import pyzen


class TileCallback(pyzen.api.RenderCallback):
    def __init__(self, engine):
        super(TileCallback, self).__init__()
        self.engine = engine
        self.rendered_tile_cnt = 0.0
        self.render_status = "Starting..."

    @staticmethod
    def convert_to_tuples(floats):
        pixels = []
        for i in range(0, len(floats), 3):
            pixels.append((floats[i], floats[i + 1], floats[i + 2], 1.0))
        return pixels

    def on_tile_end(self, film, tile_id):
        tile = film.tiles[tile_id]
        result = self.engine.begin_result(
            tile.x, tile.y,
            tile.width, tile.height)
        render_view = self.engine.active_view_get()
        layer = result.layers[0].passes.find_by_name("Combined", render_view)
        floats = tile.get_data()
        pixels = self.convert_to_tuples(floats)
        #layer.rect = [[0.1, 0.9, 0.1, 1.0]] * (result.resolution_x * result.resolution_y)
        layer.rect = pixels
        #self.engine.update_result(result)
        self.engine.end_result(result)

        self.rendered_tile_cnt += 1
        self.engine.update_progress(self.rendered_tile_cnt / film.get_tile_count())
        self.render_status = "Finished rendering tile {}".format(tile_id)