import arcade
import numpy

class Icon(arcade.Sprite):
    """An icon on the map using a texture."""
    def __init__(self, path_or_texture = None, scale = 1, center_x = 0, center_y = 0, angle = 0, icon_id = 0, text="", people_count = 0, angle_rot = 0, typename = "", unique_id = 1000, country_id = 0, **kwargs):
        super().__init__(path_or_texture, scale, center_x, center_y, angle, **kwargs)
        self.icon_id = icon_id
        self.text = text
        self.people_count = people_count
        self.angle_rot = angle_rot
        self.typename = typename
        self.unique_id = unique_id
        self.country_id = country_id

class Toast(arcade.gui.UILabel):
    """Info notification."""
    def __init__(self, text: str, duration: float = 2.0, **kwargs):
        super().__init__(**kwargs)
        self.text     = text
        self.duration = duration
        self.time     = 0

    def on_update(self, dt):
        self.time += dt

        if self.time > self.duration:
            self.parent.remove(self)

class Tile(arcade.SpriteSolidColor):
    def __init__(self, width, height, x, y, color, id_):
        super().__init__(width, height, x, y, arcade.color.WHITE)
        self.color = color
        self.id_ = id_

class GridLayer():
    """Suggestion from @typefoo"""
    def __init__(self, grid_size: tuple[int, int], tile_size: int = 10):
        self.tile_size = tile_size
        self.grid_size = grid_size
        self.grid = numpy.empty((grid_size[0], grid_size[1]), dtype=object)
        self.grid_width, self.grid_height = grid_size

    def __getitem__(self, grid_point: tuple[int, int]):
        x, y = grid_point
        if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
            return self.grid[x][y]
        return None

if __name__ == "__main__":
    print("""nation-utils, custom python file for holding reused code for several files.""")