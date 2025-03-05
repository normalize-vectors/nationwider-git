from array import array
import arcade
import arcade.gui
import arcade.gui.widgets
import numpy as np
from PIL import Image
import threading
import queue
import chunker_lz4 as chunker
from dataclasses import dataclass
import json
# display settings
WIDTH, HEIGHT = 1920, 1080
SCREEN_SIZE = (WIDTH, HEIGHT)
RESIZED_SIZE = 1920, 1080

ID_MAP = {
    (0, 0, 127)     : "0",  # WATER
    (99, 173, 95)   : "1",  # COLD PLAINS
    (52, 72, 40)    : "2",  # BOREAL FOREST
    (10, 87, 6)     : "3",  # DECIDIOUS FOREST
    (16, 59,  17)   : "4",  # CONIFEROUS FOREST
    (64, 112, 32)   : "5",  # TROPICAL FOREST
    (80, 96, 48)    : "6",  # SWAMPLAND
    (7, 154, 0)     : "7",  # PLAINS
    (12, 172, 0)    : "8",  # PRAIRIE
    (124, 156, 0)   : "9",  # SAVANNA
    (80, 80, 64)    : "10", # MARSHLAND
    (64, 80, 80)    : "11", # MOOR
    (112, 112, 64)  : "12", # STEPPE
    (64, 64, 16)    : "13", # TUNDRA
    (255, 186, 0)   : "14", # MAGMA
    (112, 80, 96)   : "15", # CANYONS
    (132, 132, 132) : "16", # MOUNTAINS
    (112, 112, 96)  : "17", # STONE DESERT
    (64, 64, 57)    : "18", # CRAGS
    (192, 192, 192) : "19", # SNOWLANDS
    (224, 224, 224) : "20", # ICE PLAINS
    (112, 112, 32)  : "21", # BRUSHLAND
    (253, 157, 24)  : "22", # RED SANDS
    (238, 224, 192) : "23", # SALT FLATS
    (255, 224, 160) : "24", # COASTAL DESERT
    (255, 208, 144) : "25", # DESERT
    (128, 64, 0)    : "26", # WETLAND
    (59, 29, 10)    : "27", # MUDLAND
    (84, 65, 65)    : "28", # HIGHLANDS/FOOTHILLS
    (26,26,26)      : "29", # POLITICAL WATER <-- redundant
    (56,56,56)      : "30", # POLITICAL LAND
}

REVERSED_ID_MAP = {
    "0"  : (0, 0, 127),      # WATER
    "1"  : (99, 173, 95),    # COLD PLAINS
    "2"  : (52, 72, 40),     # BOREAL FOREST
    "3"  : (10, 87, 6),      # DECIDUOUS FOREST
    "4"  : (16, 59, 17),     # CONIFEROUS FOREST
    "5"  : (64, 112, 32),    # TROPICAL FOREST
    "6"  : (80, 96, 48),     # SWAMPLAND
    "7"  : (7, 154, 0),      # PLAINS
    "8"  : (12, 172, 0),     # PRAIRIE
    "9"  : (124, 156, 0),    # SAVANNA
    "10" : (80, 80, 64),     # MARSHLAND
    "11" : (64, 80, 80),     # MOOR
    "12" : (112, 112, 64),   # STEPPE
    "13" : (64, 64, 16),     # TUNDRA
    "14" : (255, 186, 0),    # MAGMA
    "15" : (112, 80, 96),    # CANYONS
    "16" : (132, 132, 132),  # MOUNTAINS
    "17" : (112, 112, 96),   # STONE DESERT
    "18" : (64, 64, 57),     # CRAGS
    "19" : (192, 192, 192),  # SNOWLANDS
    "20" : (224, 224, 224),  # ICE PLAINS
    "21" : (112, 112, 32),   # BRUSHLAND
    "22" : (253, 157, 24),   # RED SANDS
    "23" : (238, 224, 192),  # SALT FLATS
    "24" : (255, 224, 160),  # COASTAL DESERT
    "25" : (255, 208, 144),  # DESERT
    "26" : (128, 64, 0),     # WETLAND
    "27" : (59, 29, 10),     # MUDLAND
    "28" : (84, 65, 65),     # HIGHLANDS/FOOTHILLS
    "29" : (26, 26, 26),     # POLITICAL WATER (redundant)
    "30" : (56, 56, 56),     # POLITICAL LAND
}

# TODO
# Terrain layer
# Political layer
# Icon layer
# be able to add notes to icons
# be able to add notes to regions < at the zoomed in layer
# LOD chunks

# 600 X 300

# hello world

@dataclass
class ChooseColor(arcade.gui.UIEvent):
    id_     : int
    id_name : str

@dataclass
class NotifyUser(arcade.gui.UIEvent):
    text    : str
    warn    : bool
    error   : bool

@dataclass
class SaveWorld(arcade.gui.UIEvent):
    save    : bool


class Toast(arcade.gui.UILabel):
    """Info notification"""
    def __init__(self, text: str, duration: float = 2.0, **kwargs):
        super().__init__(**kwargs)
        self.text     = text
        self.duration = duration
        self.time     = 0

    def on_update(self, dt):
        self.time += dt

        if self.time > self.duration:
            self.parent.remove(self)


class UIPalleteButton(arcade.gui.UIFlatButton):
    def __init__(self, *, x = 0, y = 0, width = 100, height = 50, text="", multiline=False, size_hint=None, size_hint_min=None, size_hint_max=None, style=None, id_=0, supplied_id_name="", **kwargs):
        super().__init__(x=x, y=y, width=width, height=height, text=text, multiline=multiline, size_hint=size_hint, size_hint_min=size_hint_min, size_hint_max=size_hint_max, style=style, **kwargs)
        self._id      : int = id_
        self._id_name : str = supplied_id_name

        self.register_event_type("on_choose_color")

    def on_click(self, event) -> bool:
        self.dispatch_event(
            "on_choose_color", ChooseColor(self, self._id, self._id_name)
        )
        return True

    def on_choose_color(self, event: ChooseColor):
        pass


class UISaveButton(arcade.gui.UIFlatButton):
    def __init__(self, *, x = 0, y = 0, width = 100, height = 50, text="", multiline=False, size_hint=None, size_hint_min=None, size_hint_max=None, style=None, **kwargs):
        super().__init__(x=x, y=y, width=width, height=height, text=text, multiline=multiline, size_hint=size_hint, size_hint_min=size_hint_min, size_hint_max=size_hint_max, style=style, **kwargs)

        self.register_event_type("on_click_save")

    def on_click(self, event) -> bool:
        self.dispatch_event(
            "on_click_save", SaveWorld(self, True)
        )
        return True

    def on_click_save(self, event: SaveWorld):
        pass


class Tile(arcade.SpriteSolidColor):
    def __init__(self, width, height, x, y, color, id_):
        super().__init__(width, height, x, y, arcade.color.WHITE)
        self.color = color
        self.id_ = id_


# Suggestion from @typefoo
class GridLayer():
    def __init__(self, grid_size: tuple[int, int], tile_size: int = 10):
        self.tile_size = tile_size
        self.grid_size = grid_size
        self.grid = np.empty((grid_size[0], grid_size[1]), dtype=object)
        self.grid_width, self.grid_height = grid_size

    def __getitem__(self, grid_point: tuple[int, int]):
        x, y = grid_point
        if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
            return self.grid[x][y]
        return None


def load_chunk(tilex:float, tiley:float, tiles_per_chunk:int, grid, chunkmanager) -> list:
    chunk_spritelist = []
    chunk_data = chunkmanager.fetch_chunk((tilex,tiley))
    for x in range(tiles_per_chunk):
        for y in range(tiles_per_chunk):
            if chunk_data is None:
                break
            id_ = chunk_data[x][y]
            tile = Tile(1, 1, (x+(tilex*20))-9.5, (y+(tiley*20))-9.5, (0,0,0,0), id_)
            chunk_spritelist.append(tile)
            grid[x+(tilex*20)][y+(tiley*20)] = tile
    return chunk_spritelist


def save_chunk(tilex:float, tiley:float, tiles_per_chunk:int, grid, chunkmanager):
    chunk_tiles = []
    for x in range(tiles_per_chunk):
        for y in range(tiles_per_chunk):
            tile = grid.__getitem__((round(tilex*tiles_per_chunk+x),round(tiley*tiles_per_chunk+y)))
            if not tile == None:
                chunk_tiles.append(tile.id_)
    chunkmanager.insert_chunk_masterthread((round(tilex*tiles_per_chunk),round(tiley*tiles_per_chunk)),chunk_tiles)

#

def background_loader(chunk_queue, result_queue, grid):
    while True:
        chunk_position = chunk_queue.get()
        if chunk_position is None:
            break

        returned_spritelist = load_chunk(chunk_position[0], chunk_position[1], 20, grid, lower_chunk_manager)
        result_queue.put(returned_spritelist)
        chunk_queue.task_done()


def background_saver(width, height, lower_grid, upper_grid, political_grid, lower_chunkmanager, upper_chunkmanager, political_chunkmanager):
    for x in range(width):
        if x % 10 == 0:
            print(f"Progress: {x} rows saved... {(x/width)*100.0}%")
        for y in range(height):
            save_chunk(x,y,20,lower_grid,lower_chunkmanager)
            save_chunk(x,y,1,upper_grid,upper_chunkmanager)
            save_chunk(x,y,1,political_grid,political_chunkmanager)


lower_chunk_manager = chunker.Manager("savedata_lz4/lower_chunks.db",tile_count=20,map_size=(600,300))
upper_chunk_manager = chunker.Manager("savedata_lz4/upper_chunks.db",tile_count=1,map_size=(600,300))
upper_political_manager=chunker.Manager("savedata_lz4/upper_political.db",tile_count=1,map_size=(600,300))

class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)
        arcade.enable_timings(165)

        self.camera                 = None
        self.resized_size           = 1920, 1080
        self.camera_speed           = 0.0, 0.0
        self.zoomed_speed_mod_adder = 0.0
        self.zoomed_speed_mod       = 1.0
        self.zoom_speed             = 0.0
        self.terrain_scene          = None
        self.last_pressed_screen    = None
        self.last_pressed_world     = None
        self.current_position_screen= None
        self.current_position_world = None
        self.selection_rectangle_size= 2
        self.last_interacted_tile   = None
        self.political_background   = True
        self.selected_lower_id      = 0
        self.editing_mode           = False
        self.editing_mode_size      = 4

        self.political_layer    = GridLayer((600,300)   ,20)
        self.high_terrain_layer = GridLayer((600,300)   ,20)
        self.low_terrain_layer  = GridLayer((12000,6000),1)

        geographic_icon  = arcade.load_texture("icons/geo_map_icon.png")
        political_icon   = arcade.load_texture("icons/pol_map_icon.png")
        information_icon = arcade.load_texture("icons/inf_map_icon.png")

        self.ui = arcade.gui.UIManager()
        self.ui.enable()

        anchor = self.ui.add(arcade.gui.UIAnchorLayout())
        layer_buttons = anchor.add(
            arcade.gui.UIBoxLayout(vertical=True, space_between=4),
            anchor_x="right",
            anchor_y="top"
        )

        self.toasts = anchor.add(arcade.gui.UIBoxLayout(space_between=2), anchor_x="left", anchor_y="top")
        self.toasts.with_padding(all=10)

        bottom_anchor = self.ui.add(arcade.gui.UIAnchorLayout())
        pallete_buttons = bottom_anchor.add(
            arcade.gui.UIGridLayout(
                column_count=10,
                row_count=10
                ).with_background(color=arcade.types.Color(30,30,30,255)),
            anchor_x="left",
            anchor_y="bottom"
        )

        center_anchor= self.ui.add(arcade.gui.UIAnchorLayout())
        self.popupmenu_buttons = center_anchor.add(
            arcade.gui.UIBoxLayout(vertical=True, space_between=4),
            anchor_x="center",
            anchor_y="center"
        )
        self.popupmenu_buttons.with_background(color=arcade.types.Color(20,20,20,255))
        self.popupmenu_buttons.visible = False

        save_button = UISaveButton(width=100,height=32,text="Save map")
        save_button.on_click_save = self.on_clicked_save
        self.popupmenu_buttons.add(save_button)

        self.pallete = {
            # --- 
            "WATER": 0,
            "COLD_PLAINS": 1,
            "BOREAL_FOREST": 2,
            "DECIDUOUS_FOREST": 3,
            # --- 
            "CONIFEROUS_FOREST": 4,
            "TROPICAL_FOREST": 5,
            "SWAMPLAND": 6,
            "PLAINS": 7,
            # --- 
            "PRAIRIE": 8,
            "SAVANNA": 9,
            "MARSHLAND": 10,
            "MOOR": 11,
            # --- 
            "STEPPE": 12,
            "TUNDRA": 13,
            "MAGMA": 14,
            "CANYONS": 15,
            # --- 
            "MOUNTAINS": 16,
            "STONE_DESERT": 17,
            "CRAGS": 18,
            "SNOWLANDS": 19,
            # --- 
            "ICE_PLAINS": 20,
            "BRUSHLAND": 21,
            "RED_SANDS": 22,
            "SALT_FLATS": 23,
            # --- 
            "COASTAL_DESERT": 24,
            "DESERT": 25,
            "WETLAND": 26,
            "MUDLAND": 27,
            # --- 
            "HIGHLANDS": 28
        }

        for i, (biome_name, biome_id) in enumerate(self.pallete.items()):
            rgb = REVERSED_ID_MAP.get((str(biome_id)),0)
            rgba= rgb + (255,)
            button = UIPalleteButton(height=32,width=32,id_=biome_id,text=f"",supplied_id_name=biome_name,style={
                "normal": arcade.gui.UIFlatButton.UIStyle(bg=(rgba[0],rgba[1],rgba[2],rgba[3])),
                "hover" : arcade.gui.UIFlatButton.UIStyle(bg=(rgba[0]+5,rgba[1]+5,rgba[2]+5,rgba[3])),
                "press" : arcade.gui.UIFlatButton.UIStyle(bg=(rgba[0],rgba[1],rgba[2],rgba[3]-50))
                }).with_padding(all=3)
            pallete_buttons.add(button, row=i // 10, column=i % 10)

            # connect event handler
            button.on_choose_color = self.on_color_button_choose_color

        biome_toggle = arcade.gui.UIFlatButton(text="", width=64, height=64)
        biome_toggle.add(
            child=arcade.gui.UIImage(
                texture=geographic_icon,
                width =64,
                height=64,
            ),
            anchor_x="center",
            anchor_y="center"
        )

        political_toggle = arcade.gui.UIFlatButton(text="", width=64, height=64)
        political_toggle.add(
            child=arcade.gui.UIImage(
                texture=political_icon,
                width =64,
                height=64,
            ),
            anchor_x="center",
            anchor_y="center"
        )

        information_toggle = arcade.gui.UIFlatButton(text="", width=64, height=64)
        information_toggle.add(
            child=arcade.gui.UIImage(
                texture=information_icon,
                width =64,
                height=64,
            ),
            anchor_x="center",
            anchor_y="center"
        )

        @biome_toggle.event
        def on_click(event: arcade.gui.UIOnClickEvent):
            print("Biome toggled")
            abc = self.terrain_scene.get_sprite_list("1")
            if abc.visible == True:
                abc.visible = False
            else:
                abc.visible = True

        @political_toggle.event
        def on_click(event: arcade.gui.UIOnClickEvent):
            print("Political toggled")
            abc = self.political_scene.get_sprite_list("0")
            if abc.visible == True:
                abc.visible = False
                self.political_background = False
            else:
                abc.visible = True
                self.political_background = True

        @information_toggle.event
        def on_click(event: arcade.gui.UIOnClickEvent):
            print("Information toggled")

        layer_buttons.add(information_toggle)
        layer_buttons.add(political_toggle)
        layer_buttons.add(biome_toggle)

    def on_color_button_choose_color(self, event: ChooseColor) -> bool:
        self.selected_lower_id = event.id_
        toast = Toast(f"Selected {event.id_name}", width=250)
        toast.update_font(
            font_color=arcade.uicolor.DARK_BLUE_MIDNIGHT_BLUE,
            font_size=12,
            bold=True
        )
        toast.with_background(color=arcade.uicolor.GREEN_EMERALD)
        toast.with_padding(all=10)

        self.toasts.add(toast)

        return True

    def on_notification_toast(self, message:str="", warn:bool=False, error:bool=False):
        toast = Toast(message, duration=2)
        if warn == True:
            toast.update_font(
                font_color=arcade.uicolor.WHITE,
                font_size=12,
                bold=True
            )
            toast.with_background(color=arcade.uicolor.YELLOW_ORANGE)
        elif error == True:
            toast.update_font(
                font_color=arcade.uicolor.WHITE,
                font_size=12,
                bold=True
            )
            toast.with_background(color=arcade.uicolor.RED_POMEGRANATE)
        else:
            toast.update_font(
                font_color=arcade.uicolor.WHITE,
                font_size=12,
                bold=True
            )
            toast.with_background(color=arcade.uicolor.BLUE_PETER_RIVER)
        toast.with_padding(all=10)

        self.toasts.add(toast)

    def on_clicked_save(self, event: SaveWorld):
        background_saver(600,300,self.low_terrain_layer,self.high_terrain_layer,self.political_layer,lower_chunk_manager,upper_chunk_manager,upper_political_manager)

    def setup(self):
        self.terrain_scene = arcade.Scene()
        self.political_scene=arcade.Scene()

        self.chunk_request_queue = queue.Queue()
        self.chunk_result_queue = queue.Queue()
        self.requested_chunks = set()

        self.camera = arcade.camera.Camera2D(); 
        self.camera.position = (0,0)

        self.terrain_scene.add_sprite_list("0") # <- water layer
        self.terrain_scene.add_sprite_list("1") # <- terrain layer BIG
        self.terrain_scene.add_sprite_list("2") # <- terrain layer SMALL

        self.political_scene.add_sprite_list("0")

        for x in range(600):
            for y in range(300):
                self.terrain_scene.add_sprite(
                    "0",
                    Tile(20, 20, x * 20, (y * 20), (0, 0, 127, 255), 0)
                )
        
        for x in range(600):
            for y in range(300):
                self.terrain_scene.add_sprite(
                    "0",
                    Tile(20, 20, x * 20, (y * 20) * -1, (0, 0, 127, 150), 0)
                )

        for x in range(600):
            biome_column = np.zeros(300,dtype=object)
            politic_column = np.zeros(300,dtype=object)
            if x % 50 == 0:
                print(f"Progress: {x} rows generated...")
            for y in range(300):
                chunk = upper_chunk_manager.fetch_chunk_masterthread((x,y))
                id_value = chunk.tolist()
                id_value:int = id_value[0]
                pixel_rgba = tuple(REVERSED_ID_MAP.get(id_value)) + (255,)
                world_x = x * 20
                world_y = y * 20

                if pixel_rgba == (0,0,127,255):
                    tile = Tile(20, 20, world_x, world_y, (0,0,0,0), id_value)
                    political_tile = Tile(20, 20, world_x, world_y, (56, 56, 56, 100), 30)
                else:
                    tile = Tile(20, 20, world_x, world_y, pixel_rgba, id_value)
                    political_tile = Tile(20, 20, world_x, world_y, (56, 56, 56, 255), 30)

                self.terrain_scene.add_sprite("1",tile)
                self.political_scene.add_sprite("0", political_tile)
                biome_column[y] = tile
                politic_column[y] = political_tile

            self.high_terrain_layer.grid[x] = biome_column
            self.political_layer.grid[x] = politic_column

        # Start the worker thread with both request and result queues
        loader_thread = threading.Thread(
            target=background_loader, 
            args=(self.chunk_request_queue, self.chunk_result_queue, self.low_terrain_layer.grid), 
            daemon=True
        )
        loader_thread.start()

    def on_resize(self, width, height):
        self.resized_size = width, height
        print(f"resized {width} and {height}")
        return super().on_resize(width, height)

    def on_update(self, dt):
        self.camera.position += (self.camera_speed[0]*self.zoomed_speed_mod, self.camera_speed[1]*self.zoomed_speed_mod)

        self.camera.zoom += self.zoom_speed*self.camera.zoom

        self.zoomed_speed_mod = max(self.zoomed_speed_mod+self.zoomed_speed_mod_adder, 0.01)
        self.zoomed_speed_mod = min(self.zoomed_speed_mod, 2.0)

        abd = self.terrain_scene.get_sprite_list("1")

        if self.camera.zoom > 2.5:
            if abd.visible == True:
                low_terrain = self.terrain_scene.get_sprite_list("2")
                low_terrain.visible = True
            else:
                low_terrain = self.terrain_scene.get_sprite_list("2")
                low_terrain.visible = False

            list_of_chunks = []
            for a in range(4):
                for b in range(4):
                    camera_tile = (round(((self.camera.position.x/20)+a)-2),round(((self.camera.position.y/20)+b)-2))
                    if not (camera_tile[0],camera_tile[1]) in self.requested_chunks:
                        list_of_chunks.append((camera_tile[0],camera_tile[1]))
                        self.requested_chunks.add((camera_tile[0],camera_tile[1]))

            for chunk in list_of_chunks:
                self.chunk_request_queue.put(chunk)

            list_of_chunks.clear()
        else:
            low_terrain = self.terrain_scene.get_sprite_list("2")
            low_terrain.visible = False

        self.process_completed_chunks()

    def process_completed_chunks(self):
        try:
            for _ in range(1):
                if self.chunk_result_queue.empty():
                    break
                    
                received_sprite_list = self.chunk_result_queue.get()
            
                for tile in received_sprite_list:
                    self.terrain_scene.add_sprite("2",tile)
                
                self.chunk_result_queue.task_done()
                
        except queue.Empty:
            pass

    def on_draw(self):
        self.camera.use() 
        self.clear() 
        self.terrain_scene.draw(pixelated=True)

        if self.political_background == True:
            arcade.draw_lbwh_rectangle_filled(-10,-10,12000,6000,(0,0,0,255))

        self.political_scene.draw(pixelated=True)

        if self.editing_mode == False:
            if self.last_pressed_world:
                if self.current_position_world:
                    # selection rectangle coordinates
                    left = min(self.last_pressed_world[0], self.current_position_world[0])
                    right = max(self.last_pressed_world[0], self.current_position_world[0])
                    bottom = min(self.last_pressed_world[1], self.current_position_world[1])
                    top = max(self.last_pressed_world[1], self.current_position_world[1])

                    arcade.draw_lrbt_rectangle_outline(left, right, bottom, top, arcade.color.ORIOLES_ORANGE, self.selection_rectangle_size)
                    # ^ drawing the selection

        if self.current_position_world:
            crosshair_size = (self.editing_mode_size/8)
            crosshair_sprite = arcade.Sprite("crosshair.png",(crosshair_size,crosshair_size),self.current_position_world[0],self.current_position_world[1],0)
            arcade.draw_sprite(crosshair_sprite,pixelated=True)
        
        self.ui.draw()

    def on_key_press(self, symbol, modifier):
        if symbol   == arcade.key.W or symbol == arcade.key.UP:
            self.camera_speed = (self.camera_speed[0], 10.0)
        elif symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.camera_speed = (-10.0, self.camera_speed[1])
        elif symbol == arcade.key.S or symbol == arcade.key.DOWN:
            self.camera_speed = (self.camera_speed[0], -10.0)
        elif symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.camera_speed = (10.0, self.camera_speed[1])

        if symbol   == arcade.key.KEY_0:
            self.zoomed_speed_mod_adder = 0.01
        if symbol   == arcade.key.KEY_9:
            self.zoomed_speed_mod_adder = -0.01

        if symbol   == arcade.key.O:
            self.editing_mode = not self.editing_mode

        if symbol   == arcade.key.ESCAPE:
            self.popupmenu_buttons.visible = not self.popupmenu_buttons.visible
        
        if symbol == arcade.key.F:
            # User hits f. Flip between full and not full screen.
            self.set_fullscreen(not self.fullscreen)
        
        if symbol == arcade.key.MINUS or symbol == arcade.key.NUM_SUBTRACT:
            if self.camera.zoom >= 0.1 and self.camera.zoom <= 0.125:
                pass
            else:
                self.zoom_speed = -0.01

        if symbol == arcade.key.EQUAL or symbol == arcade.key.NUM_ADD:
            self.zoom_speed = 0.01

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.W or symbol == arcade.key.S or symbol == arcade.key.UP or symbol == arcade.key.DOWN:
            self.camera_speed = (self.camera_speed[0], 0.0)
        elif symbol == arcade.key.A or symbol == arcade.key.D or symbol == arcade.key.LEFT or symbol == arcade.key.RIGHT:
            self.camera_speed = (0.0, self.camera_speed[1])

        if symbol == arcade.key.EQUAL or symbol == arcade.key.NUM_ADD:
            self.zoom_speed = 0.0
        if symbol == arcade.key.MINUS or symbol == arcade.key.NUM_SUBTRACT:
            self.zoom_speed = 0.0

        if symbol == arcade.key.KEY_0 or symbol == arcade.key.KEY_9:
            self.zoomed_speed_mod_adder = 0

    def on_mouse_press(self, x, y, button, modifiers):
        if button is arcade.MOUSE_BUTTON_LEFT:
            self.last_pressed_screen = (x, y)
            diff_fr_res = (SCREEN_SIZE[0]-self.resized_size[0])/2, (SCREEN_SIZE[1]-self.resized_size[1])/2

            # Conversion from screen coordinates to world coordinates
            world_x = ((((x - self.width  / 2)-diff_fr_res[0]) / self.camera.zoom) + self.camera.position.x) 
            world_y = ((((y - self.height / 2)-diff_fr_res[1]) / self.camera.zoom) + self.camera.position.y)
            # x -> origin point changed to the center with '/2' -> zoom amount -> camera offset 
            self.last_pressed_world = (world_x, world_y)

            tile_x = round(world_x / 20)
            tile_y = round(world_y / 20)
            clicked_tile = self.high_terrain_layer.__getitem__((tile_x, tile_y))

            if self.editing_mode == True:
                list_of_tiles = np.zeros((self.editing_mode_size,self.editing_mode_size), dtype=object)
                if not self.editing_mode_size <= 1:
                    half_size = self.editing_mode_size // 2
                    radius = half_size

                    for x_offset in range(self.editing_mode_size):
                        for y_offset in range(self.editing_mode_size):
                            x_ = world_x + (x_offset - half_size)
                            y_ = world_y + (y_offset - half_size)

                            distance = ((x_offset - half_size) + 0.5) ** 2 + ((y_offset - half_size) + 0.5) ** 2

                            if distance <= (radius + 0.5) ** 2:
                                list_of_tiles[x_offset, y_offset] = self.low_terrain_layer.__getitem__((round(x_ + 9.5), round(y_ + 9.5)))
                            else:
                                list_of_tiles[x_offset, y_offset] = None 
                else:
                    list_of_tiles[0] = self.low_terrain_layer.__getitem__((round(world_x + 9.5), round(world_y + 9.5)))

                for x_ in range(self.editing_mode_size):
                    for y_ in range(self.editing_mode_size):
                        if not list_of_tiles[x_][y_] is None:
                            list_of_tiles[x_][y_].id_ = self.selected_lower_id
                            pixel_rgba = REVERSED_ID_MAP.get(str(self.selected_lower_id),(0,0,0)) + (255,)
                            list_of_tiles[x_][y_].color = pixel_rgba
                        else:
                            print(f"no tiles returned to selection ...")

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        camera = self.camera
        zoom = camera.zoom #
        if buttons is arcade.MOUSE_BUTTON_RIGHT:
            camera.position -= (dx / zoom, dy / zoom)
        if buttons is arcade.MOUSE_BUTTON_LEFT:
            self.current_position_screen = (x, y)
            camera_x, camera_y = camera.position
            diff_fr_res = (SCREEN_SIZE[0]-self.resized_size[0])/2, (SCREEN_SIZE[1]-self.resized_size[1])/2
            # Conversion from screen coordinates to world coordinates
            world_x = ((((x - self.width  / 2)-diff_fr_res[0]) / self.camera.zoom) + camera_x) 
            world_y = ((((y - self.height / 2)-diff_fr_res[1]) / self.camera.zoom) + camera_y)
            # x -> origin point changed to the center with '/2' -> zoom amount -> camera offset 

            self.current_position_world = (world_x, world_y)

            if self.editing_mode == True:
                list_of_tiles = np.zeros((self.editing_mode_size,self.editing_mode_size), dtype=object)
                if not self.editing_mode_size <= 1:
                    half_size = self.editing_mode_size // 2
                    radius = half_size

                    for x_offset in range(self.editing_mode_size):
                        for y_offset in range(self.editing_mode_size):
                            x_ = world_x + (x_offset - half_size)
                            y_ = world_y + (y_offset - half_size)

                            distance = ((x_offset - half_size) + 0.5) ** 2 + ((y_offset - half_size) + 0.5) ** 2

                            if distance <= (radius + 0.5) ** 2:
                                list_of_tiles[x_offset, y_offset] = self.low_terrain_layer.__getitem__((round(x_ + 9.5), round(y_ + 9.5)))
                            else:
                                list_of_tiles[x_offset, y_offset] = None 
                else:
                    list_of_tiles[0] = self.low_terrain_layer.__getitem__((round(world_x + 9.5), round(world_y + 9.5)))

                for x_ in range(self.editing_mode_size):
                    for y_ in range(self.editing_mode_size):
                        if not list_of_tiles[x_][y_] is None:
                            list_of_tiles[x_][y_].id_ = self.selected_lower_id
                            pixel_rgba = REVERSED_ID_MAP.get(str(self.selected_lower_id),(0,0,0)) + (255,)
                            list_of_tiles[x_][y_].color = pixel_rgba
                        else:
                            print(f"no tiles returned to list? ...")

    def on_mouse_release(self, x, y, button, modifiers):
        if button is arcade.MOUSE_BUTTON_LEFT:
            self.last_pressed_world = None
            self.last_pressed_screen = None

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if self.editing_mode == False:
            if self.camera.zoom >= 0.1 and self.camera.zoom <= 0.125:
                if scroll_y == 1.0:
                    self.camera.zoom += 0.1*self.camera.zoom
                    self.zoomed_speed_mod -= 0.01
            else:
                if scroll_y == 1.0:
                    self.camera.zoom += 0.1*self.camera.zoom
                    self.zoomed_speed_mod -= 0.01

                if scroll_y == -1.0:
                    self.camera.zoom -= 0.1*self.camera.zoom
                    self.zoomed_speed_mod += 0.01
        else:
            if self.editing_mode_size == 1:
                if scroll_y == 1.0:
                    self.editing_mode_size += 1
            else:
                self.editing_mode_size += int(scroll_y)
        
    def on_mouse_motion(self, x, y, dx, dy):
        self.current_position_screen = (x, y)
        diff_fr_res = (SCREEN_SIZE[0]-self.resized_size[0])/2, (SCREEN_SIZE[1]-self.resized_size[1])/2
        
        # Conversion from screen coordinates to world coordinates
        world_x = ((((x - self.width  / 2)-diff_fr_res[0]) / self.camera.zoom) + self.camera.position.x) 
        world_y = ((((y - self.height / 2)-diff_fr_res[1]) / self.camera.zoom) + self.camera.position.y)
        # x -> origin point changed to the center with '/2' -> zoom amount -> camera offset 
        self.current_position_world = (world_x, world_y)

        tile_x = round(world_x / 20)
        tile_y = round(world_y / 20)
        self.last_interacted_tile = self.high_terrain_layer.__getitem__((tile_x, tile_y))

    def cleanup(self):
        self.chunk_result_queue.shutdown()
        self.chunk_request_queue.shutdown()


def main():
    game = Game(WIDTH, HEIGHT, "NEONATION")
    game.setup()
    arcade.run()
    game.cleanup()


if __name__ == "__main__":
    main()
    