from array import array
import math
import arcade
import arcade.gui
import arcade.gui.widgets
import numpy as np
from PIL import Image
import threading
import queue
from dataclasses import dataclass
import json
import random
# display settings
WIDTH, HEIGHT = 1920, 1080
SCREEN_SIZE = (WIDTH, HEIGHT)
RESIZED_SIZE = 1920, 1080

ID_MAP = {
    (0,0,0)         : 255,# CLEAR TILE [ NONE ]
    (0, 0, 127)     : 0,  # WATER
    (99, 173, 95)   : 1,  # COLD PLAINS
    (52, 72, 40)    : 2,  # BOREAL FOREST
    (10, 87, 6)     : 3,  # DECIDIOUS FOREST
    (16, 59,  17)   : 4,  # CONIFEROUS FOREST
    (64, 112, 32)   : 5,  # TROPICAL FOREST
    (80, 96, 48)    : 6,  # SWAMPLAND
    (7, 154, 0)     : 7,  # PLAINS
    (12, 172, 0)    : 8,  # PRAIRIE
    (124, 156, 0)   : 9,  # SAVANNA
    (80, 80, 64)    : 10, # MARSHLAND
    (64, 80, 80)    : 11, # MOOR
    (112, 112, 64)  : 12, # STEPPE
    (64, 64, 16)    : 13, # TUNDRA
    (255, 186, 0)   : 14, # MAGMA
    (112, 80, 96)   : 15, # CANYONS
    (132, 132, 132) : 16, # MOUNTAINS
    (112, 112, 96)  : 17, # STONE DESERT
    (64, 64, 57)    : 18, # CRAGS
    (192, 192, 192) : 19, # SNOWLANDS
    (224, 224, 224) : 20, # ICE PLAINS
    (112, 112, 32)  : 21, # BRUSHLAND
    (253, 157, 24)  : 22, # RED SANDS
    (238, 224, 192) : 23, # SALT FLATS
    (255, 224, 160) : 24, # COASTAL DESERT
    (255, 208, 144) : 25, # DESERT
    (128, 64, 0)    : 26, # WETLAND
    (59, 29, 10)    : 27, # MUDLAND
    (84, 65, 65)    : 28, # HIGHLANDS/FOOTHILLS
    # SOUTH MAP ADDITIONS
    (170, 153, 153) : 29, # ABYSSAL WASTE
    (182, 170, 191) : 30, # PALE WASTE
    (51, 102, 153)  : 31, # ELYSIAN FOREST
    (10, 59, 59)    : 32, # ELYSIAN JUNGLE
    (203, 99, 81)   : 33, # VOLCANIC WASTES
    (121, 32, 32)   : 34, # IGNEOUS ROCKLAND
    (59, 10, 10)    : 35, # CRIMSON FOREST
    (192, 176, 80)  : 36, # FUNGAL FOREST
    (153, 204, 0)   : 37, # SULFURIC FIELDS
    (240, 240, 187) : 38, # LIMESTONE DESERT
    (255, 163, 255) : 39, # DIVINE FIELDS
    (170, 48, 208)  : 40, # DIVINE MEADOW
    (117, 53, 144)  : 41, # DIVINE WOODLAND
    (102, 32, 137)  : 42 # DIVINE EDEN
}

REVERSED_ID_MAP = {
    255: (0, 0, 0),       # CLEAR TILE [ NONE ]
    254: (53, 53, 53),    # POLITICAL LAND
    253: (53, 53, 53),    # POLITICAL WATER
    0: (0, 0, 127),       # WATER
    1: (99, 173, 95),     # COLD PLAINS
    2: (52, 72, 40),      # BOREAL FOREST
    3: (10, 87, 6),       # DECIDUOUS FOREST
    4: (16, 59, 17),      # CONIFEROUS FOREST
    5: (64, 112, 32),     # TROPICAL FOREST
    6: (80, 96, 48),      # SWAMPLAND
    7: (7, 154, 0),       # PLAINS
    8: (12, 172, 0),      # PRAIRIE
    9: (124, 156, 0),     # SAVANNA
    10: (80, 80, 64),     # MARSHLAND
    11: (64, 80, 80),     # MOOR
    12: (112, 112, 64),   # STEPPE
    13: (64, 64, 16),     # TUNDRA
    14: (255, 186, 0),    # MAGMA
    15: (112, 80, 96),    # CANYONS
    16: (132, 132, 132),  # MOUNTAINS
    17: (112, 112, 96),   # STONE DESERT
    18: (64, 64, 57),     # CRAGS
    19: (192, 192, 192),  # SNOWLANDS
    20: (224, 224, 224),  # ICE PLAINS
    21: (112, 112, 32),   # BRUSHLAND
    22: (253, 157, 24),   # RED SANDS
    23: (238, 224, 192),  # SALT FLATS
    24: (255, 224, 160),  # COASTAL DESERT
    25: (255, 208, 144),  # DESERT
    26: (128, 64, 0),     # WETLAND
    27: (59, 29, 10),     # MUDLAND
    28: (84, 65, 65),     # HIGHLANDS/FOOTHILLS
    # SOUTH MAP ADDITIONS
    29: (170, 153, 153),  # ABYSSAL WASTE
    30: (182, 170, 191),  # PALE WASTE
    31: (51, 102, 153),   # ELYSIAN FOREST
    32: (10, 59, 59),     # ELYSIAN JUNGLE
    33: (203, 99, 81),    # VOLCANIC WASTES
    34: (121, 32, 32),    # IGNEOUS ROCKLAND
    35: (59, 10, 10),     # CRIMSON FOREST
    36: (192, 176, 80),   # FUNGAL FOREST
    37: (153, 204, 0),    # SULFURIC FIELDS
    38: (240, 240, 187),  # LIMESTONE DESERT
    39: (255, 163, 255),  # DIVINE FIELDS
    40: (170, 48, 208),   # DIVINE MEADOW
    41: (117, 53, 144),   # DIVINE WOODLAND
    42: (102, 32, 137)    # DIVINE EDEN
}

REVERSED_POLITICAL_ID_MAP = {
    0   :   (53, 53, 53), 
    1   :   (121, 7, 18), # DRAGONEGGLOL
    2   :   (42, 86, 18), # UMM
    3   :   (183, 197, 215), # WATBOI
    4   :   (20, 209, 136), # ASIMPLECREATOR
    5   :   (193, 38, 38), # CATARMOUR
    6   :   (63, 63, 116), # BALLISTICMISSILE
    7   :   (0,0,0),
}

ICON_ID_MAP = {
    0: "icons/structures/str_village",
    1: "icons/structures/str_town",
    2: "icons/structures/str_city",
    3: "icons/structures/str_metro",
    4: "icons/structures/str_outpost",
    5: "icons/structures/str_keep",
    6: "icons/structures/str_fortress",
    7: "icons/structures/str_bastion",
    8: "icons/info/info_note",
}

# ---

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

# ---

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

# ---

class PlaceIcon(arcade.Sprite):
    def __init__(self, path_or_texture = None, scale = 1, center_x = 0, center_y = 0, angle = 0, icon_id = 0, text="", **kwargs):
        super().__init__(path_or_texture, scale, center_x, center_y, angle, **kwargs)
        self.icon_id = icon_id
        self.text = text

class VesselIcon(arcade.Sprite):
    def __init__(self, path_or_texture = None, scale = 1, center_x = 0, center_y = 0, angle = 0, icon_id = 0, troop_count = 0, **kwargs):
        super().__init__(path_or_texture, scale, center_x, center_y, angle, **kwargs)
        self.icon_id = icon_id
        self.troop_count = troop_count

class TroopIcon(arcade.Sprite):
    def __init__(self, path_or_texture = None, scale = 1, center_x = 0, center_y = 0, angle = 0, icon_id = 0, troop_count = 0, **kwargs):
        super().__init__(path_or_texture, scale, center_x, center_y, angle, **kwargs)
        self.icon_id = icon_id
        self.troop_count = troop_count

# ---

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
        self.grid = np.empty((grid_size[0], grid_size[1]), dtype=object)
        self.grid_width, self.grid_height = grid_size

    def __getitem__(self, grid_point: tuple[int, int]):
        x, y = grid_point
        if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
            return self.grid[x][y]
        return None

# ---

class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)
        self.camera                 = arcade.camera.Camera2D(); 
        self.camera.position        = (0,0)
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
        self.selection_rectangle_size=1
        self.last_interacted_tile   = None
        self.political_background   = True
        self.selected_lower_id      = 0
        self.editing_mode           = False
        self.editing_mode_size      = 4

        self.selected_icon_id       = None
        self.selected_world_icon    = None
        self.moving_the_icon        = False

        self.terrain_scene          = arcade.Scene()
        self.political_scene        = arcade.Scene()
        self.info_scene             = arcade.Scene()

        self.chunk_request_queue    = queue.Queue()
        self.chunk_result_queue     = queue.Queue()
        self.requested_chunks       = set()

        self.terrain_scene.add_sprite_list("0") # <- water layer
        self.terrain_scene.add_sprite_list("1") # <- terrain layer BIG
        self.terrain_scene.add_sprite_list("2") # <- terrain layer SMALL

        self.info_scene.add_sprite_list("0")
        self.info_scene_list = []

        self.political_scene.add_sprite_list("0")

        self.ui = arcade.gui.UIManager()
        self.ui.enable()

        anchor = self.ui.add(arcade.gui.UIAnchorLayout())
        self.toasts = anchor.add(arcade.gui.UIBoxLayout(space_between=2), anchor_x="left", anchor_y="top")
        self.toasts.with_padding(all=10)

        # < - DEFINING GRIDS FOR ALL LAYERS #GRIDS
        self.political_layer    = GridLayer((600,300)   ,20)
        self.high_terrain_layer = GridLayer((600,300)   ,20)
        self.low_terrain_layer  = GridLayer((12000,6000),1)

        self.s_political_layer    = GridLayer((600,300),20)
        self.s_high_terrain_layer = GridLayer((600,300),20)
        self.icons                    = {
            'locations': []
        }
        # -

        # < - LOADING DATA FROM FILE #LOAD
        loaded_data = np.load("shareddata/mapdata.npz",allow_pickle=True)
        self.loaded_id_grid             = loaded_data['a']
        self.loaded_id_grid_political   = loaded_data['b']
        self.loaded_id_grid_small       = loaded_data['c']

        self.s_loaded_id_grid           = loaded_data['aa']
        self.s_loaded_id_grid_political = loaded_data['bb']
            # < south doesnt have more detail for now >

        self.icons_array                = loaded_data['cc']
        self.icons = self.icons_array.item()
        # -

        geographic_icon  = arcade.load_texture("icons/geo_map_icon.png")
        political_icon   = arcade.load_texture("icons/pol_map_icon.png")
        information_icon = arcade.load_texture("icons/inf_map_icon.png")

        self.icon_data_anchor = self.ui.add(arcade.gui.UIAnchorLayout())
        self.icon_description = self.icon_data_anchor.add(
            arcade.gui.UIBoxLayout(
                vertical=True,
                space_between=4
            ),
            anchor_x="right",
            anchor_y="center"
        )
        self.move_button_icon = arcade.load_texture("icons/move_icon.png")
        self.remove_button_icon = arcade.load_texture("icons/remove_icon.png")

        self.mouse_click_anchor = self.ui.add(arcade.gui.UIAnchorLayout())
        self.mouse_click_anchor.visible = False
        self.menu_options = self.mouse_click_anchor.add(
            arcade.gui.UIGridLayout(
                column_count=5,
                row_count=5,
                vertical_spacing=4,
                horizontal_spacing=4
                ).with_background(color=arcade.types.Color(10,10,10,100)),
            anchor_x="center",
            anchor_y="center"
        )

        village_icon = arcade.load_texture(f"{ICON_ID_MAP.get(0)}_64x64.png")
        add_str_village = arcade.gui.UIFlatButton(text="", width=64, height=64)
        add_str_village.add(
            child=arcade.gui.UIImage(
                texture=village_icon,
                width =64,
                height=64,
            ),
            anchor_x="center",
            anchor_y="center"
        )

        town_icon = arcade.load_texture(f"{ICON_ID_MAP.get(1)}_64x64.png")
        add_str_town = arcade.gui.UIFlatButton(text="", width=64, height=64)
        add_str_town.add(
            child=arcade.gui.UIImage(
                texture=town_icon,
                width =64,
                height=64,
            ),
            anchor_x="center",
            anchor_y="center"
        )

        city_icon = arcade.load_texture(f"{ICON_ID_MAP.get(2)}_64x64.png")
        add_str_city = arcade.gui.UIFlatButton(text="", width=64, height=64)
        add_str_city.add(
            child=arcade.gui.UIImage(
                texture=city_icon,
                width =64,
                height=64,
            ),
            anchor_x="center",
            anchor_y="center"
        )

        metro_icon = arcade.load_texture(f"{ICON_ID_MAP.get(3)}_64x64.png")
        add_str_metro = arcade.gui.UIFlatButton(text="", width=64, height=64)
        add_str_metro.add(
            child=arcade.gui.UIImage(
                texture=metro_icon,
                width =64,
                height=64,
            ),
            anchor_x="center",
            anchor_y="center"
        )

        outpost_icon = arcade.load_texture(f"{ICON_ID_MAP.get(4)}_64x64.png")
        add_str_outpost = arcade.gui.UIFlatButton(text="", width=64, height=64)
        add_str_outpost.add(
            child=arcade.gui.UIImage(
                texture=outpost_icon,
                width =64,
                height=64,
            ),
            anchor_x="center",
            anchor_y="center"
        )

        keep_icon = arcade.load_texture(f"{ICON_ID_MAP.get(5)}_64x64.png")
        add_str_keep = arcade.gui.UIFlatButton(text="", width=64, height=64)
        add_str_keep.add(
            child=arcade.gui.UIImage(
                texture=keep_icon,
                width =64,
                height=64,
            ),
            anchor_x="center",
            anchor_y="center"
        )

        fortress_icon = arcade.load_texture(f"{ICON_ID_MAP.get(6)}_64x64.png")
        add_str_fortress = arcade.gui.UIFlatButton(text="", width=64, height=64)
        add_str_fortress.add(
            child=arcade.gui.UIImage(
                texture=fortress_icon,
                width =64,
                height=64,
            ),
            anchor_x="center",
            anchor_y="center"
        )

        bastion_icon = arcade.load_texture(f"{ICON_ID_MAP.get(7)}_64x64.png")
        add_str_bastion = arcade.gui.UIFlatButton(text="", width=64, height=64)
        add_str_bastion.add(
            child=arcade.gui.UIImage(
                texture=bastion_icon,
                width =64,
                height=64,
            ),
            anchor_x="center",
            anchor_y="center"
        )

        note_icon = arcade.load_texture(f"{ICON_ID_MAP.get(8)}_64x64.png")
        add_info_note = arcade.gui.UIFlatButton(text="", width=64, height=64)
        add_info_note.add(
            child=arcade.gui.UIImage(
                texture=note_icon,
                width =64,
                height=64,
            ),
            anchor_x="center",
            anchor_y="center"
        )

        self.menu_options.add(add_str_village,  0, 0)
        self.menu_options.add(add_str_town,     1, 0)
        self.menu_options.add(add_str_city,     2, 0)
        self.menu_options.add(add_str_metro,    3, 0)
        self.menu_options.add(add_str_outpost,  4, 0)
        self.menu_options.add(add_str_keep,     0, 1)
        self.menu_options.add(add_str_fortress, 1, 1)
        self.menu_options.add(add_str_bastion,  2, 1)
        self.menu_options.add(add_info_note,    3, 1)

        @add_str_village.event
        def on_click(event: arcade.gui.UIOnClickEvent):
            self.selected_icon_id = 0
            self.mouse_click_anchor.visible = False

        @add_str_town.event
        def on_click(event: arcade.gui.UIOnClickEvent):
            self.selected_icon_id = 1
            self.mouse_click_anchor.visible = False

        @add_str_city.event
        def on_click(event: arcade.gui.UIOnClickEvent):
            self.selected_icon_id = 2
            self.mouse_click_anchor.visible = False

        @add_str_metro.event
        def on_click(event: arcade.gui.UIOnClickEvent):
            self.selected_icon_id = 3
            self.mouse_click_anchor.visible = False

        @add_str_outpost.event
        def on_click(event: arcade.gui.UIOnClickEvent):
            self.selected_icon_id = 4
            self.mouse_click_anchor.visible = False

        @add_str_keep.event
        def on_click(event: arcade.gui.UIOnClickEvent):
            self.selected_icon_id = 5
            self.mouse_click_anchor.visible = False

        @add_str_fortress.event
        def on_click(event: arcade.gui.UIOnClickEvent):
            self.selected_icon_id = 6
            self.mouse_click_anchor.visible = False

        @add_str_bastion.event
        def on_click(event: arcade.gui.UIOnClickEvent):
            self.selected_icon_id = 7
            self.mouse_click_anchor.visible = False

        @add_info_note.event
        def on_click(event: arcade.gui.UIOnClickEvent):
            self.selected_icon_id = 8
            self.mouse_click_anchor.visible = False

        layer_buttons = anchor.add(
            arcade.gui.UIBoxLayout(vertical=True, space_between=4),
            anchor_x="right",
            anchor_y="top"
        )

        bottom_anchor = self.ui.add(arcade.gui.UIAnchorLayout())
        pallete_buttons = bottom_anchor.add(
            arcade.gui.UIGridLayout(
                column_count=10,
                row_count=10
                ).with_background(color=arcade.types.Color(30,30,30,255)),
            anchor_x="left",
            anchor_y="bottom"
        )

        center_anchor = self.ui.add(arcade.gui.UIAnchorLayout())
        self.popupmenu_buttons = center_anchor.add(
            arcade.gui.UIBoxLayout(vertical=True, space_between=4),
            anchor_x="center",
            anchor_y="center"
        )
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
            "HIGHLANDS": 28,
            "ABYSSAL_WASTE": 29,
            "PALE_WASTE": 30,
            "ELYSIAN_FOREST": 31,
            # --- 
            "ELYSIAN_JUNGLE": 32,
            "VOLCANIC_WASTES": 33,
            "IGNEOUS_ROCKLAND": 34,
            "CRIMSON_FOREST": 35,
            # --- 
            "FUNGAL_FOREST": 36,
            "SULFURIC_FIELDS": 37,
            "LIMESTONE_DESERT": 38,
            "DIVINE_FIELDS": 39,
            # --- 
            "DIVINE_MEADOW": 40,
            "DIVINE_WOODLAND": 41,
            "DIVINE_EDEN": 42
            # ...
            # --- 
        }

        for i, (biome_name, biome_id) in enumerate(self.pallete.items()):
            rgb = REVERSED_ID_MAP.get(biome_id,0)
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
            bcd = self.info_scene.get_sprite_list("0")
            if bcd.visible == True:
                bcd.visible = False
            else:
                bcd.visible = True

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
        toast = Toast(message, duration=4)

        toast.update_font(
            font_color=arcade.uicolor.BLACK,
            font_size=12,
            bold=True
        )
        toast.with_background(color=arcade.uicolor.BLUE_PETER_RIVER)

        if warn == True:
            toast.update_font(
                font_color=arcade.uicolor.BLACK,
                font_size=12,
                bold=True
            )
            toast.with_background(color=arcade.uicolor.YELLOW_ORANGE)
        if error == True:
            toast.update_font(
                font_color=arcade.uicolor.BLACK,
                font_size=12,
                bold=True
            )
            toast.with_background(color=arcade.uicolor.RED_POMEGRANATE)

        toast.with_padding(all=10)

        self.toasts.add(toast)

    def on_clicked_save(self, event: SaveWorld):
        #SAVE
        try:
            np.savez_compressed("shareddata/mapdata.npz",a=self.loaded_id_grid,b=self.loaded_id_grid_political,c=self.loaded_id_grid_small,aa=self.s_loaded_id_grid,bb=self.s_loaded_id_grid_political,cc=np.array(self.icons))
            self.on_notification_toast("Saved map ...")
        except:
            self.on_notification_toast("Failed to save map ...",error=True)

    def background_loader(self, chunk_queue, result_queue, grid, id_grid):
        while True:
            chunk_position = chunk_queue.get()
            if chunk_position is None:
                break

            tilex, tiley = chunk_position
            returned_spritelist = self.load_chunk(tilex, tiley, 20, grid, id_grid)
            
            # Add to result queue
            result_queue.put((tilex, tiley, returned_spritelist))
            chunk_queue.task_done()

    def load_chunk(self, tilex: int, tiley: int, tiles_per_chunk: int, grid, id_grid) -> list:
        chunk_spritelist = []
        chunk_data = np.zeros((tiles_per_chunk,tiles_per_chunk),dtype=np.uint8)
        for _x_ in range(tiles_per_chunk):
            for _y_ in range(tiles_per_chunk):
                chunk_data[_x_][_y_] = id_grid[_x_+tilex*tiles_per_chunk][_y_+tiley*tiles_per_chunk]

        for x in range(tiles_per_chunk):
            for y in range(tiles_per_chunk):
                try:
                    id_ = chunk_data[x][y]
                    world_x = x+tilex*20
                    world_y = y+tiley*20
                    if id_ == 255:
                        pixel_rgba = (0,0,0,0)
                    else:
                        pixel_rgba = REVERSED_ID_MAP.get(id_, (0, 0, 0)) + (255,)

                    tile = Tile(1, 1, world_x-9.5, world_y-9.5, pixel_rgba, id_)
                    chunk_spritelist.append(tile)

                    grid[world_x][world_y] = tile

                except IndexError:
                    print(f"Warning: Chunk ({tilex}, {tiley}) has missing data at ({x}, {y})")

        return chunk_spritelist

    def process_completed_chunks(self):
        try:
            for _ in range(1):
                if self.chunk_result_queue.empty():
                    break
                    
                tilex, tiley, received_sprite_list = self.chunk_result_queue.get()
            
                for tile in received_sprite_list:
                    self.terrain_scene.add_sprite("2",tile)
                
                self.chunk_result_queue.task_done()
                
        except queue.Empty:
            pass

    def find_icon_near(self, x, y, radius=5):
        """Finds the closest icon within the given radius."""
        if not self.info_scene_list:
            return None
        
        icons_within_radius = [
            icon for icon in self.info_scene_list
            if math.sqrt((icon.position[0] - x) ** 2 + (icon.position[1] - y) ** 2) <= radius
        ]

        if not icons_within_radius:
            return None

        return min(
            icons_within_radius,
            key=lambda icon: math.sqrt((icon.position[0] - x) ** 2 + (icon.position[1] - y) ** 2)
        )

    def setup(self):
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
                    Tile(20, 20, x * 20, (y * 20) * -1, (0, 0, 127, 225), 0)
                )

        for x in range(600):
            biome_column = np.zeros(300,dtype=object)
            politic_column = np.zeros(300,dtype=object)
            if x % 50 == 0:
                print(f"+ Progress: {x} rows loaded...")
            for y in range(300):
                id_value = self.loaded_id_grid[x][y]
                political_value = self.loaded_id_grid_political[x][y]
                political_rgb = REVERSED_POLITICAL_ID_MAP.get(political_value,(53,53,53))
                pixel_rgb = REVERSED_ID_MAP.get(id_value,0)
                world_x = x * 20
                world_y = y * 20

                if id_value == 0:
                    tile = Tile(20, 20, world_x, world_y, (0,0,0,0), id_value)
                    political_tile = Tile(20, 20, world_x, world_y, political_rgb+(100,), 253)
                else:
                    tile = Tile(20, 20, world_x, world_y, pixel_rgb+(255,), id_value)
                    political_tile = Tile(20, 20, world_x, world_y, political_rgb+(255,), 254)

                self.terrain_scene.add_sprite("1",tile)
                self.political_scene.add_sprite("0", political_tile)
                
                biome_column[y]     = tile
                politic_column[y]   = political_tile

            self.high_terrain_layer.grid[x] = biome_column
            self.political_layer.grid[x]    = politic_column

        for x in range(600):
            biome_column = np.zeros(300,dtype=object)
            politic_column = np.zeros(300,dtype=object)
            if x % 50 == 0:
                print(f"+ Progress: {x} rows loaded...")
            for y in range(300):
                id_value = self.s_loaded_id_grid[y][x]
                political_value = self.s_loaded_id_grid_political[x][y]
                political_rgb = REVERSED_POLITICAL_ID_MAP.get(political_value,(53,53,53))
                pixel_rgb = REVERSED_ID_MAP.get(id_value,0)
                world_x = x * 20
                world_y = ((y * 20)*-1)-20

                if id_value == 0:
                    tile            = Tile(20, 20, world_x, world_y, (0,0,0,0), id_value)
                    political_tile  = Tile(20, 20, world_x, world_y, political_rgb+(100,), political_value)
                else:
                    tile            = Tile(20, 20, world_x, world_y, pixel_rgb+(255,), id_value)
                    political_tile  = Tile(20, 20, world_x, world_y, political_rgb+(255,), political_value)

                self.terrain_scene.add_sprite("1",tile)
                self.political_scene.add_sprite("0", political_tile)
                
                biome_column[y] = tile
                politic_column[y] = political_tile

            self.s_high_terrain_layer.grid[x] = biome_column
            self.s_political_layer.grid[x] = biome_column

        for icon in self.icons['locations']:
            icon_path = str(ICON_ID_MAP.get(icon['id']))+"_64x64.png"
            icon = PlaceIcon(icon_path,1,icon['x'],icon['y'],0,icon['id'],icon['text'])
            self.info_scene.add_sprite("0",icon)
            self.info_scene_list.append(icon)

        loader_thread = threading.Thread(
            target=self.background_loader, 
            args=(self.chunk_request_queue, self.chunk_result_queue, self.low_terrain_layer.grid, self.loaded_id_grid_small), 
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

        for icon in self.info_scene_list:
            icon.scale = max(1.0-(self.camera.zoom/3),0.05)

    def on_draw(self):
        self.camera.use() 
        self.clear() 
        self.terrain_scene.draw(pixelated=True)

        if self.political_background == True:
            arcade.draw_lbwh_rectangle_filled(-10,-10,12000,6000,(0,0,0,255))
            arcade.draw_lbwh_rectangle_filled(-10,-10,12000,-6000,(0,0,0,255))

        self.political_scene.draw(pixelated=True)

        self.info_scene.draw(pixelated=True)

        if self.selected_world_icon:
            arcade.draw_circle_outline(self.selected_world_icon.position[0],self.selected_world_icon.position[1],max(32-(self.camera.zoom),8),(255,255,255,255),1,0,5)

        if self.editing_mode == False:
            if self.moving_the_icon == False:
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
            if self.editing_mode == True:
                crosshair_size = (self.editing_mode_size/8)
                crosshair_sprite = arcade.Sprite("crosshair.png",(crosshair_size,crosshair_size),self.current_position_world[0],self.current_position_world[1],0)
                arcade.draw_sprite(crosshair_sprite,pixelated=True)
            else:
                arcade.draw_circle_outline(self.current_position_world[0],self.current_position_world[1],4,(255,255,255,255),1,0,4)
        
        self.ui.draw()

    def on_key_press(self, symbol, modifier):
        if symbol == arcade.key.R:
            print(self.requested_chunks)
            self.requested_chunks = set()
            print(self.requested_chunks)
            print(f"+ Clearing generated chunks ...")

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

        if symbol   == arcade.key.SLASH:
            #if self.editing_mode == True:
            self.mouse_click_anchor.visible = True

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

            if self.editing_mode == True:
                if self.selected_icon_id:
                    icon_path = str(ICON_ID_MAP.get(self.selected_icon_id))+"_64x64.png"
                    icon = PlaceIcon(icon_path,1,world_x,world_y,0,self.selected_icon_id,"")
                    self.info_scene.add_sprite("0",icon)
                    self.info_scene_list.append(icon)
                    self.icons["locations"].append({
                        "id": self.selected_icon_id,
                        "x": round(world_x),
                        "y": round(world_y),
                        "text": ""
                    })
                    self.selected_icon_id = None
                else:
                    list_of_tiles = np.zeros((self.editing_mode_size,self.editing_mode_size), dtype=object)
                    list_of_tile_positions = []

                    half_size = self.editing_mode_size // 2
                    radius = half_size

                    for x_offset in range(self.editing_mode_size):
                        for y_offset in range(self.editing_mode_size):
                            x_ = world_x + (x_offset - half_size)
                            y_ = world_y + (y_offset - half_size)

                            distance = ((x_offset - half_size) + 0.5) ** 2 + ((y_offset - half_size) + 0.5) ** 2

                            if not self.editing_mode_size == 1:
                                if distance <= (radius + 0.5) ** 2:
                                    list_of_tiles[x_offset, y_offset] = self.low_terrain_layer.__getitem__((round(x_ + 9.5), round(y_ + 9.5)))
                                    list_of_tile_positions.append((round(x_ + 9.5), round(y_ + 9.5)))
                                else:
                                    list_of_tiles[x_offset, y_offset] = None 
                            else:
                                list_of_tiles[x_offset, y_offset] = self.low_terrain_layer.__getitem__((round(x_ + 9.5), round(y_ + 9.5)))
                                list_of_tile_positions.append((round(x_ + 9.5), round(y_ + 9.5)))

                    for x_ in range(self.editing_mode_size):
                        for y_ in range(self.editing_mode_size):
                            if not list_of_tiles[x_][y_] is None:
                                pixel_rgba = REVERSED_ID_MAP.get(self.selected_lower_id,(0,0,0)) + (255,)
                                list_of_tiles[x_][y_].color = pixel_rgba
                            else:
                                print(f"no tiles returned to selection ...")
                    
                    print(list_of_tile_positions)
                    if not list_of_tile_positions is None:
                        for tile in list_of_tile_positions:
                            print(f"tile[0] {tile[0]} + tile[1] {tile[1]}")
                            self.loaded_id_grid_small[tile[0],tile[1]] = self.selected_lower_id

            else:
                nearby_icon = self.find_icon_near(world_x, world_y, radius=10)
                if nearby_icon:
                    print(f"Found {nearby_icon}")
                    self.selected_world_icon = nearby_icon
                    self.icon_description.clear()
                    label = arcade.gui.UITextArea(
                        text=f"Info:\n{nearby_icon.text}",
                        multiline=True,
                        width=64,
                        height=128
                    ).with_background(color=arcade.types.Color(20,20,20,255)).with_border(width=1,color=arcade.types.Color(40,40,40,255))
                    move_button = arcade.gui.UIFlatButton(text="", width=64, height=64)
                    move_button.add(
                        child=arcade.gui.UIImage(
                            texture=self.move_button_icon,
                            width =64,
                            height=64,
                        ),
                        anchor_x="center",
                        anchor_y="center"
                    )
                    remove_button = arcade.gui.UIFlatButton(text="", width=64, height=64)
                    remove_button.add(
                        child=arcade.gui.UIImage(
                            texture=self.remove_button_icon,
                            width =64,
                            height=64,
                        ),
                        anchor_x="center",
                        anchor_y="center"
                    )
                    edit_button_icon = arcade.load_texture("icons/edit_icon.png")
                    edit_text_button = arcade.gui.UIFlatButton(text="",width=16,height=16)
                    edit_text_button.add(
                        child=arcade.gui.UIImage(
                            texture=edit_button_icon,
                            width =8,
                            height=8,
                        ),
                        anchor_x="center",
                        anchor_y="center"
                    )
                    @edit_text_button.event
                    def on_click(event: arcade.gui.UIOnClickEvent):
                        text_input = self.icon_description.add(
                            arcade.gui.UIInputText(
                                width=200,
                                height=64,
                                font_size=12,
                                border_color=arcade.uicolor.GRAY_CONCRETE,
                                border_width=2
                            ).with_background(color=arcade.types.Color(20,20,20,255))
                        )

                        @text_input.event("on_change")
                        def on_text_change(event: arcade.gui.UIOnChangeEvent):
                            nearby_icon.text = event.new_value

                    @move_button.event
                    def on_click(event: arcade.gui.UIOnClickEvent):
                        self.moving_the_icon = True
                        print(f"moving icon ...")

                    @remove_button.event
                    def on_click(event: arcade.gui.UIOnClickEvent):
                        self.info_scene_list.remove(self.selected_world_icon)
                        abc = self.info_scene.get_sprite_list("0")
                        abc.remove(self.selected_world_icon)
                        index = 0
                        for icon in self.icons['locations']:
                            if icon['x'] == self.selected_world_icon.position[0] and icon['y'] == self.selected_world_icon.position[1]:
                                self.icons['locations'].pop(index)
                            else:
                                index+=1

                        self.selected_world_icon = None

                    self.icon_description.add(label)
                    self.icon_description.add(move_button)
                    self.icon_description.add(remove_button)
                    self.icon_description.add(edit_text_button)
                else:
                    print("No icons found nearby.")
                    self.selected_world_icon = None
                    self.icon_description.clear()

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
                list_of_tile_positions = []

                half_size = self.editing_mode_size // 2
                radius = half_size

                for x_offset in range(self.editing_mode_size):
                    for y_offset in range(self.editing_mode_size):
                        x_ = world_x + (x_offset - half_size)
                        y_ = world_y + (y_offset - half_size)

                        distance = ((x_offset - half_size) + 0.5) ** 2 + ((y_offset - half_size) + 0.5) ** 2

                        if not self.editing_mode_size == 1:
                            if distance <= (radius + 0.5) ** 2:
                                list_of_tiles[x_offset, y_offset] = self.low_terrain_layer.__getitem__((round(x_ + 9.5), round(y_ + 9.5)))
                                list_of_tile_positions.append((round(x_ + 9.5), round(y_ + 9.5)))
                            else:
                                list_of_tiles[x_offset, y_offset] = None 
                        else:
                            list_of_tiles[x_offset, y_offset] = self.low_terrain_layer.__getitem__((round(x_ + 9.5), round(y_ + 9.5)))
                            list_of_tile_positions.append((round(x_ + 9.5), round(y_ + 9.5)))

                for x_ in range(self.editing_mode_size):
                    for y_ in range(self.editing_mode_size):
                        if not list_of_tiles[x_][y_] is None:
                            pixel_rgba = REVERSED_ID_MAP.get(self.selected_lower_id,(0,0,0)) + (255,)
                            list_of_tiles[x_][y_].color = pixel_rgba
                        else:
                            print(f"no tiles returned to selection ...")
                
                print(list_of_tile_positions)
                if not list_of_tile_positions is None:
                    for tile in list_of_tile_positions:
                        print(f"tile[0] {tile[0]} + tile[1] {tile[1]}")
                        self.loaded_id_grid_small[tile[0],tile[1]] = self.selected_lower_id
            else:
                if self.moving_the_icon == True:
                    index = 0
                    for icon in self.icons['locations']:
                        if icon['x'] == self.selected_world_icon.position[0] and icon['y'] == self.selected_world_icon.position[1]:
                            icon['x'] = world_x
                            icon['y'] = world_y
                        else:
                            index+=1
                    self.selected_world_icon.position = (world_x,world_y)

    def on_mouse_release(self, x, y, button, modifiers):
        if button is arcade.MOUSE_BUTTON_LEFT:
            self.last_pressed_world = None
            self.last_pressed_screen = None
            self.moving_the_icon = False

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

# ---

def main():
    game = Game(WIDTH, HEIGHT, "NATIONWIDER")
    game.setup()
    arcade.run()
    game.cleanup()


if __name__ == "__main__":
    main()
    