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
    0   :   (53, 53, 53), # wilderness
    1   :   (121, 7, 18),
    2   :   (42, 86, 18),
    3   :   (183, 197, 215),
    4   :   (20, 209, 136),
    5   :   (193, 38, 38),
    6   :   (63, 63, 116), # Aurimukstis1
    7   :   (10, 41, 93),
    8   :   (18, 158, 165),
    9   :   (20, 55, 17),
    10  :   (196, 153, 0),
    11  :   (243, 104, 6),
    12  :   (84, 198, 223),
    13  :   (95, 22, 151),
    14  :   (48, 114, 214),
    15  :   (78, 104, 77),
    16  :   (0, 112, 141),
    17  :   (243, 145, 51)
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
    # -
    8: "icons/info/info_note",
    9: "icons/info/info_line",
    # - 
    10:"icons/units/vessel_raft",
    11:"icons/units/vessel_cog",
    12:"icons/units/vessel_yawl",
    13:"icons/units/vessel_brig",
    14:"icons/units/vessel_corvette",
    15:"icons/units/vessel_frigate",
    16:"icons/units/vessel_cruiser",
    17:"icons/units/vessel_battleship",
    18:"icons/units/vessel_dreadnought",
    19:"icons/units/vessel_carrier",
    # -
    20:"icons/units/unit_0.1k",
    21:"icons/units/unit_1k",
    22:"icons/units/unit_5k",
    23:"icons/units/unit_10k",
    24:"icons/units/unit_100k",
    # -
    25:"icons/units/unit_artillery",
    26:"icons/units/unit_cavalry",
    27:"icons/units/unit_heavy_artillery",
    28:"icons/units/unit_heavy_cavalry",
    29:"icons/units/unit_heavy_infantry",
    30:"icons/units/unit_infantry",
    31:"icons/units/unit_ranged_cavalry",
    32:"icons/units/unit_ranged_infantry",
    33:"icons/units/unit_skirmishers"
}

print(ICON_ID_MAP)

# ---

@dataclass
class ChooseColor(arcade.gui.UIEvent):
    id_     : int
    id_name : str

@dataclass
class ChooseCountry(arcade.gui.UIEvent):
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

class UICountryButton(arcade.gui.UIFlatButton):
    def __init__(self, *, x = 0, y = 0, width = 100, height = 50, text="", multiline=False, size_hint=None, size_hint_min=None, size_hint_max=None, style=None, id_=0, supplied_id_name="", **kwargs):
        super().__init__(x=x, y=y, width=width, height=height, text=text, multiline=multiline, size_hint=size_hint, size_hint_min=size_hint_min, size_hint_max=size_hint_max, style=style, **kwargs)
        self._id      : int = id_
        self._id_name : str = supplied_id_name

        self.register_event_type("on_choose_country")

    def on_click(self, event) -> bool:
        self.dispatch_event(
            "on_choose_country", ChooseCountry(self, self._id, self._id_name)
        )
        return True

    def on_choose_country(self, event: ChooseCountry):
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

class Infocon(arcade.Sprite):
    def __init__(self, path_or_texture = None, scale = 1, center_x = 0, center_y = 0, angle = 0, icon_id = 0, text="", people_count = 0, angle_rot = 0, typename = "", unique_id = 1000, country_id = 0, **kwargs):
        super().__init__(path_or_texture, scale, center_x, center_y, angle, **kwargs)
        self.icon_id = icon_id
        self.text = text
        self.people_count = people_count
        self.angle_rot = angle_rot
        self.typename = typename
        self.unique_id = unique_id
        self.country_id = country_id

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
        #INIT
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
        self.selected_country_id    = 0
        self.editing_mode           = False
        self.editing_mode_size      = 4

        self.previous_angle         = 0

        self.selected_icon_id       = None
        self.selected_world_icon    = None
        self.moving_the_icon        = False
        self.rotating_the_icon      = False

        self.selected_line          = None
        self.drawing_line_start     = None
        self.drawing_line_end       = None

        self.terrain_scene          = arcade.Scene()
        self.political_scene        = arcade.Scene()
        self.info_scene             = arcade.Scene()

        self.chunk_request_queue    = queue.Queue()
        self.chunk_result_queue     = queue.Queue()
        self.requested_chunks       = set()

        self.terrain_scene.add_sprite_list("0")
        self.terrain_scene.add_sprite_list("1")
        self.terrain_scene.add_sprite_list("2") 

        self.info_scene.add_sprite_list("0")
        self.info_scene_list = []

        self.political_scene.add_sprite_list("0")

        self.ui = arcade.gui.UIManager()
        self.ui.enable()

        anchor = self.ui.add(arcade.gui.UIAnchorLayout())
        self.toasts = anchor.add(arcade.gui.UIBoxLayout(space_between=2), anchor_x="left", anchor_y="top")
        self.toasts.with_padding(all=10)

        # < - DEFINING GRIDS FOR ALL LAYERS #GRIDS
        self.political_layer        = GridLayer((600,300)   ,20)
        self.upper_terrain_layer    = GridLayer((600,300)   ,20)
        self.lower_terrain_layer    = GridLayer((12000,6000),1)

        self.s_political_layer      = GridLayer((600,300)   ,20)
        self.s_upper_terrain_layer  = GridLayer((600,300)   ,20)
        self.icons = {
            'locations': [],
            'lines': []
        }
        # -

        # < - LOADING DATA FROM FILE #LOAD
        loaded_data = np.load("shareddata/converted_mapdata.npz",allow_pickle=True)
        loaded_a_data                   = loaded_data['a']
        self.upper_terrain_layer.grid[:]= loaded_a_data

        loaded_b_data                   = loaded_data['b']
        self.political_layer.grid[:]    = loaded_b_data

        loaded_c_data                   = loaded_data['c']
        self.lower_terrain_layer.grid[:]= loaded_c_data

        loaded_a_s_data                 = loaded_data['a_s']
        self.s_upper_terrain_layer.grid[:]=loaded_a_s_data

        loaded_b_s_data                 = loaded_data['b_s']
        self.s_political_layer.grid[:]  = loaded_b_s_data

        self.icons_array                = loaded_data['cc']
        self.icons = self.icons_array.item()
        # -

        geographic_icon  = arcade.load_texture("icons/geo_map_icon.png")
        political_icon   = arcade.load_texture("icons/pol_map_icon.png")
        information_icon = arcade.load_texture("icons/inf_map_icon.png")
        geographic_palette_icon = arcade.load_texture("icons/geo_palette_icon.png")
        political_palette_icon  = arcade.load_texture("icons/pol_palette_icon.png")

        self.icon_data_anchor = self.ui.add(arcade.gui.UIAnchorLayout())
        self.icon_description = self.icon_data_anchor.add(
            arcade.gui.UIBoxLayout(
                vertical=False,
                space_between=2
            ),
            anchor_x="center",
            anchor_y="bottom"
        )

        self.mouse_click_anchor = self.ui.add(arcade.gui.UIAnchorLayout())
        self.mouse_click_anchor.visible = False
        self.menu_options = self.mouse_click_anchor.add(
            arcade.gui.UIGridLayout(
                column_count=10,
                row_count=10,
                vertical_spacing=1,
                horizontal_spacing=1
                ).with_background(color=arcade.types.Color(10,10,10,255)).with_border(color=arcade.types.Color(30,30,30,255)),
            anchor_x="center",
            anchor_y="center"
        )

        icon_names = [
            "village", "town", "city", "metro", "outpost",
            "keep", "fortress", "bastion", "note", "line",
            "raft", "cog", "yawl", "brig", "corvette",
            "frigate", "cruiser", "battleship", "dreadnought", "carrier",
            "0.1k unit", "1k unit", "5k unit", "10k unit", "100k unit",
            "artillery", "cavarly", "heavy artillery", "heavy cavalry", "heavy infantry",
            "infantry", "ranged cavalry", "ranged infantry", "skirmishers"
        ]

        self.buttons = []

        for idx, name in enumerate(icon_names):
            icon_texture = arcade.load_texture(f"{ICON_ID_MAP.get(idx)}.png")
            button = arcade.gui.UIFlatButton(text="", width=64, height=64)
            button.add(
                child=arcade.gui.UIImage(texture=icon_texture, width=64, height=64),
                anchor_x="center",
                anchor_y="center"
            )
            self.menu_options.add(button, idx % 10, idx // 10)
            self.buttons.append(button)

            @button.event
            def on_click(event: arcade.gui.UIOnClickEvent, idx=idx, name=name):
                self.selected_icon_id = idx
                self.on_notification_toast(f"Selected {name}")

        layer_buttons = anchor.add(
            arcade.gui.UIBoxLayout(vertical=True, space_between=4),
            anchor_x="right",
            anchor_y="top"
        )

        bottom_anchor = self.ui.add(arcade.gui.UIAnchorLayout())
        biome_palette_buttons = bottom_anchor.add(
            arcade.gui.UIBoxLayout(
                vertical=False
                ).with_background(color=arcade.types.Color(30,30,30,255)),
            anchor_x="center",
            anchor_y="bottom"
        )
        country_palette_buttons = bottom_anchor.add(
            arcade.gui.UIBoxLayout(
                vertical=False
                ).with_background(color=arcade.types.Color(30,30,30,255)),
            anchor_x="center",
            anchor_y="bottom"
        )
        biome_palette_buttons.visible = False
        country_palette_buttons.visible = False

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

        self.country_pallete =  {
            "wilderness"        : 0,
            "DragonEgglol"      : 1,
            "Hoovyzepoot"       : 2,
            "Watboi"            : 3,
            "ASimpleCreator"    : 4,
            "Catarmour"         : 5,
            "Aurimukstis1"      : 6,
            "Tuna"              : 7,
            "Rubidianlabs"      : 8,
            "LightningBMW"      : 9,
            "N2H4"              : 10,
            "Loiosh"            : 11,
            "Antigrain"         : 12,
            "AVeryBigNurd"      : 13,
            "Superbantom"       : 14,
            "NuttyMCNuttzz"     : 15,
            "Raven314"          : 16,
            "Spikey_boy"        : 17
                                }

        for i, (biome_name, biome_id) in enumerate(self.pallete.items()):
            rgb = REVERSED_ID_MAP.get(biome_id,0)
            rgba= rgb + (255,)
            button = UIPalleteButton(height=32,width=32,id_=biome_id,text=f"",supplied_id_name=biome_name,style={
                "normal": arcade.gui.UIFlatButton.UIStyle(bg=(rgba[0],rgba[1],rgba[2],rgba[3])),
                "hover" : arcade.gui.UIFlatButton.UIStyle(bg=(rgba[0]+5,rgba[1]+5,rgba[2]+5,rgba[3])),
                "press" : arcade.gui.UIFlatButton.UIStyle(bg=(rgba[0],rgba[1],rgba[2],rgba[3]-50))
                })
            biome_palette_buttons.add(button)

            # connect event handler
            button.on_choose_color = self.on_color_button_choose_color

        for i, (country_owner, country_id) in enumerate(self.country_pallete.items()):
            rgb = REVERSED_POLITICAL_ID_MAP.get(country_id,0)
            rgba= rgb + (255,)
            button = UICountryButton(height=32,width=32,id_=country_id,text=f"",supplied_id_name=country_owner,style={
                "normal": arcade.gui.UIFlatButton.UIStyle(bg=(rgba[0],rgba[1],rgba[2],rgba[3])),
                "hover" : arcade.gui.UIFlatButton.UIStyle(bg=(rgba[0]+5,rgba[1]+5,rgba[2]+5,rgba[3])),
                "press" : arcade.gui.UIFlatButton.UIStyle(bg=(rgba[0],rgba[1],rgba[2],rgba[3]-50))
                })
            country_palette_buttons.add(button)

            # connect event handler
            button.on_choose_country = self.on_country_button_choose_country

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

        biome_palette_toggle = arcade.gui.UIFlatButton(text="", width=64, height=64)
        biome_palette_toggle.add(
            child=arcade.gui.UIImage(
                texture=geographic_palette_icon,
                width =64,
                height=64,
            ),
            anchor_x="center",
            anchor_y="center"
        )

        political_palette_toggle = arcade.gui.UIFlatButton(text="", width=64, height=64)
        political_palette_toggle.add(
            child=arcade.gui.UIImage(
                texture=political_palette_icon,
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

        @biome_palette_toggle.event
        def on_click(event: arcade.gui.UIOnClickEvent):
            if country_palette_buttons.visible == True:
                country_palette_buttons.visible = False
                biome_palette_buttons.visible = True
            else:
                biome_palette_buttons.visible = not biome_palette_buttons.visible

        @political_palette_toggle.event
        def on_click(event: arcade.gui.UIOnClickEvent):
            if biome_palette_buttons.visible == True:
                biome_palette_buttons.visible = False
                country_palette_buttons.visible = True
            else:
                country_palette_buttons.visible = not country_palette_buttons.visible

        layer_buttons.add(information_toggle)
        layer_buttons.add(political_toggle)
        layer_buttons.add(biome_toggle)
        layer_buttons.add(biome_palette_toggle)
        layer_buttons.add(political_palette_toggle)

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
    
    def on_country_button_choose_country(self, event: ChooseCountry) -> bool:
        self.selected_country_id = event.id_
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
        try:
            self.on_notification_toast("Trying to save map ...")
            a_grid = np.empty((600,300),dtype=np.uint8)
            a_grid = np.empty((600,300),dtype=np.uint8)
            c_grid = np.empty((12000, 6000), dtype=np.uint8)

            def extract_id(cell):
                return cell.id_ if isinstance(cell, Tile) else cell
            
            def extract_country_id(cell):
                return cell.id_ if isinstance(cell, Tile) else cell
            
            extract_attribute_biome = np.vectorize(extract_id, otypes=[np.uint8])
            extract_attribute_country = np.vectorize(extract_country_id, otypes=[np.uint8])
            a_grid = extract_attribute_biome(self.upper_terrain_layer.grid)
            b_grid = extract_attribute_country(self.political_layer.grid)
            c_grid = extract_attribute_biome(self.lower_terrain_layer.grid)

            a_s_grid = extract_attribute_biome(self.s_upper_terrain_layer.grid)
            b_s_grid = extract_attribute_country(self.s_political_layer.grid)
            np.savez_compressed("shareddata/converted_mapdata.npz",
                                a=a_grid,
                                b=b_grid,
                                c=c_grid,
                                a_s=a_s_grid,
                                b_s=b_s_grid,
                                cc=np.array(self.icons)
                                )
            self.on_notification_toast(f"{type(self.lower_terrain_layer.grid)}",warn=True)
            self.on_notification_toast(f"{type(self.upper_terrain_layer.grid)}",warn=True)
            self.on_notification_toast(f"{type(self.political_layer.grid)}",warn=True)
            self.on_notification_toast(f"{type(self.s_upper_terrain_layer.grid)}",warn=True)
            self.on_notification_toast(f"{type(self.s_political_layer.grid)}",warn=True)
            self.on_notification_toast("Saved map ...")
        except Exception as e: 
            self.on_notification_toast("Failed to save map ... "+str(e),error=True)

    def background_loader(self, chunk_queue, result_queue, grid):
        while True:
            chunk_position = chunk_queue.get()
            if chunk_position is None:
                break

            tilex, tiley = chunk_position
            returned_spritelist = self.load_chunk(tilex, tiley, 20, grid)
            
            # Add to result queue
            result_queue.put((tilex, tiley, returned_spritelist))
            chunk_queue.task_done()

    def load_chunk(self, tilex: int, tiley: int, tiles_per_chunk: int, grid) -> list:
        chunk_spritelist = []
        chunk_data = np.zeros((tiles_per_chunk,tiles_per_chunk),dtype=np.uint8)
        for _x_ in range(tiles_per_chunk):
            for _y_ in range(tiles_per_chunk):
                chunk_data[_x_][_y_] = grid[_x_+tilex*tiles_per_chunk][_y_+tiley*tiles_per_chunk]

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
    
    def find_line_near(self, x, y, radius=5):
        """Finds closest line within given radius."""
        if not self.icons['lines']:
            return None
        
        lines_within_radius = [
            line for line in self.icons['lines']
            if math.sqrt((line[0][0] - x) ** 2 + (line[0][1] - y) ** 2) <= radius
        ]

        if not lines_within_radius:
            return None
        
        return min(
            lines_within_radius,
            key=lambda line: math.sqrt((line[0][0] - x) ** 2 + (line[0][1] - y) ** 2)
        )

    def setup(self):
        print("Loading background map [1/3]")
        for x in range(600):
            if x % 50 == 0:
                print(f"+ Progress: {x} background rows loaded...")
            for y in range(300):
                self.terrain_scene.add_sprite(
                    "0",
                    Tile(20, 20, x * 20, (y * 20), (0, 0, 127, 255), 0)
                )
                self.terrain_scene.add_sprite(
                    "0",
                    Tile(20, 20, x * 20, (y * 20) * -1, (0, 0, 127, 225), 0)
                )

        print("Loading north map [2/3]")
        for x in range(600):
            if x % 50 == 0:
                print(f"+ Progress: {x} north rows loaded...")
            for y in range(300):
                tile_id_value = self.upper_terrain_layer.grid[x][y]
                political_tile_id_value = self.political_layer.grid[x][y]
                pixel_rgb = REVERSED_ID_MAP.get(tile_id_value,(255,255,255))
                political_rgb = REVERSED_POLITICAL_ID_MAP.get(political_tile_id_value,(53,53,53))
                world_x = (x * 20)
                world_y = (y * 20)

                if tile_id_value == 0:
                    tile = Tile(20, 20, world_x, world_y, (0,0,0,0), tile_id_value)
                    political_tile = Tile(20, 20, world_x, world_y, political_rgb+(100,), political_tile_id_value)
                else:
                    tile = Tile(20, 20, world_x, world_y, pixel_rgb+(255,), tile_id_value)
                    political_tile = Tile(20, 20, world_x, world_y, political_rgb+(255,), political_tile_id_value)

                self.terrain_scene.add_sprite("1",tile)
                self.political_scene.add_sprite("0", political_tile)
            
                self.upper_terrain_layer.grid[x][y] = tile
                self.political_layer.grid[x][y] = political_tile

        # print("Loading south map [3/3]")
        # for x in range(600):
        #     if x % 50 == 0:
        #         print(f"+ Progress: {x} south rows loaded...")
        #     for y in range(300):
        #         tile_id_value = self.s_upper_terrain_layer.grid[x][y]
        #         political_tile_id_value = self.s_political_layer.grid[x][y]
        #         pixel_rgb = REVERSED_ID_MAP.get(tile_id_value,(255,255,255))
        #         political_rgb = REVERSED_POLITICAL_ID_MAP.get(political_tile_id_value,(53,53,53))
        #         world_x = (x * 20)
        #         world_y = (y * 20)-6000

        #         if tile_id_value == 0:
        #             tile            = Tile(20, 20, world_x, world_y, (0,0,0,0), tile_id_value)
        #             political_tile  = Tile(20, 20, world_x, world_y, political_rgb+(100,), political_tile_id_value)
        #         else:
        #             tile            = Tile(20, 20, world_x, world_y, pixel_rgb+(255,), tile_id_value)
        #             political_tile  = Tile(20, 20, world_x, world_y, political_rgb+(255,), political_tile_id_value)

        #         self.terrain_scene.add_sprite("1",tile)
        #         self.political_scene.add_sprite("0", political_tile)

        #         self.s_upper_terrain_layer.grid[x][y] = tile
        #         self.s_political_layer.grid[x][y] = political_tile    

        for icon in self.icons['locations']:
            icon_path = str(ICON_ID_MAP.get(icon['id']))+".png"
            icon_object = Infocon(icon_path,1,
                           icon['x'],
                           icon['y'],
                           0.0,
                           icon['id'],
                           icon['text'],
                           icon['people_count'],
                           icon['angle_rot'],
                           icon['typename'],
                           icon['unique_id'],
                           icon['country_id']
                        )
            icon_object.angle = icon['angle_rot']
            self.info_scene.add_sprite("0",icon_object)
            self.info_scene_list.append(icon_object)

        loader_thread = threading.Thread(
            target=self.background_loader, 
            args=(self.chunk_request_queue, self.chunk_result_queue, self.lower_terrain_layer.grid), 
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
            for a in range(6):
                for b in range(6):
                    camera_tile = (round(((self.camera.position.x/20)+a)-3),round(((self.camera.position.y/20)+b)-3))
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
            if icon.icon_id >= 25 and icon.icon_id <= 33:
                icon.scale = max(1.0-(self.camera.zoom/3),0.003)
            else:
                icon.scale = max(1.0-(self.camera.zoom/3),0.05)

    def on_draw(self):
        self.camera.use() 
        self.clear() 
        self.terrain_scene.draw(pixelated=True)

        if self.political_background == True:
            arcade.draw_lbwh_rectangle_filled(-10,-10,12000,6000,(0,0,0,255))
            arcade.draw_lbwh_rectangle_filled(-10,-10,12000,-6000,(0,0,0,255))

        self.political_scene.draw(pixelated=True)

        for start, end in self.icons['lines']:
            arcade.draw_line(start[0],start[1],end[0],end[1],(255,0,0,255),line_width=0.1)

        self.info_scene.draw(pixelated=True)

        if self.selected_world_icon:

            if self.rotating_the_icon:
                arcade.draw_circle_outline(self.selected_world_icon.position[0],self.selected_world_icon.position[1],max(32-(self.camera.zoom*3),4),(255,255,255,255),1,0,12)
            elif self.moving_the_icon:
                arcade.draw_circle_outline(self.selected_world_icon.position[0],self.selected_world_icon.position[1],max(32-(self.camera.zoom*3),4),(255,255,255,255),1,0,4)
            else:
                arcade.draw_circle_outline(self.selected_world_icon.position[0],self.selected_world_icon.position[1],max(32-(self.camera.zoom*3),4),(255,255,255,255),1,0,6)

        if self.selected_line:
            arcade.draw_lbwh_rectangle_outline(self.selected_line[0]-2,self.selected_line[1]-2,4,4,(255,255,255,255),0.1)

        if self.current_position_world:
            if self.editing_mode == True:
                if self.camera.zoom >= 2.5:
                    crosshair_size = (self.editing_mode_size/8)
                    crosshair_sprite = arcade.Sprite("crosshair.png",(crosshair_size,crosshair_size),self.current_position_world[0],self.current_position_world[1],0)
                    arcade.draw_sprite(crosshair_sprite,pixelated=True)
                    arcade.draw_lrbt_rectangle_outline(round(self.current_position_world[0]-0.5),round(self.current_position_world[0]+0.5),round(self.current_position_world[1]-0.5),round(self.current_position_world[1]+0.5),color=(255,255,255,255),border_width=0.1)
                else:
                    arcade.draw_lbwh_rectangle_outline(round(self.current_position_world[0]/20)*20-10,round(self.current_position_world[1]/20)*20-10,20,20,(255,255,255,255),1)
            else:
                arcade.draw_circle_outline(self.current_position_world[0],self.current_position_world[1],2,(255,255,255,255),0.2,0,-1)
        
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

        if symbol   == arcade.key.KEY_1:
            icons_spritelist = self.info_scene.get_sprite_list("0")
            icons_spritelist.visible = not icons_spritelist.visible
        if symbol   == arcade.key.KEY_2:
            political_spritelist = self.political_scene.get_sprite_list("0")
            political_spritelist.visible = not political_spritelist.visible
            self.political_background = not self.political_background
        if symbol   == arcade.key.KEY_3:
            biome_spritelist = self.terrain_scene.get_sprite_list("1")
            biome_spritelist_2=self.terrain_scene.get_sprite_list("2")
            biome_spritelist.visible = not biome_spritelist.visible
            biome_spritelist_2.visible = not biome_spritelist_2.visible
        if symbol   == arcade.key.KEY_0:
            self.zoomed_speed_mod_adder = 0.01
        if symbol   == arcade.key.KEY_9:
            self.zoomed_speed_mod_adder = -0.01

        if symbol   == arcade.key.O:
            self.editing_mode = not self.editing_mode
        if symbol   == arcade.key.F:
            self.set_fullscreen(not self.fullscreen)
        if symbol   == arcade.key.M:
            if self.rotating_the_icon == True:
                self.rotating_the_icon = False
                self.moving_the_icon = True
            else:
                self.moving_the_icon = not self.moving_the_icon
        if symbol   == arcade.key.R:
            if self.moving_the_icon == True:
                self.moving_the_icon = False
                self.rotating_the_icon = True
            else:
                self.rotating_the_icon = not self.rotating_the_icon

        if symbol   == arcade.key.E:
            self.mouse_click_anchor.visible = not self.mouse_click_anchor.visible
        if symbol   == arcade.key.ESCAPE:
            self.popupmenu_buttons.visible = not self.popupmenu_buttons.visible
        
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
        if button is arcade.MOUSE_BUTTON_RIGHT:
            if self.selected_icon_id or self.selected_icon_id == 0:
                self.selected_icon_id = None
                self.on_notification_toast("Deselected icon id.",warn=True)
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

            if self.editing_mode == True:
                if self.camera.zoom >= 2.5:
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
                                    list_of_tiles[x_offset, y_offset] = self.lower_terrain_layer.__getitem__((round(x_ + 9.5), round(y_ + 9.5)))
                                    list_of_tile_positions.append((round(x_ + 9.5), round(y_ + 9.5)))
                                else:
                                    list_of_tiles[x_offset, y_offset] = None 
                            else:
                                list_of_tiles[x_offset, y_offset] = self.lower_terrain_layer.__getitem__((round(x_ + 9.5), round(y_ + 9.5)))
                                list_of_tile_positions.append((round(x_ + 9.5), round(y_ + 9.5)))

                    for x_ in range(self.editing_mode_size):
                        for y_ in range(self.editing_mode_size):
                            if not list_of_tiles[x_][y_] is None:
                                pixel_rgba = REVERSED_ID_MAP.get(self.selected_lower_id,(0,0,0)) + (255,)
                                list_of_tiles[x_][y_].color = pixel_rgba
                                list_of_tiles[x_][y_].id_ = self.selected_lower_id
                            else:
                                print(f"no tiles returned to selection ...")
                
                elif self.camera.zoom < 2.5:
                    political_tile_to_edit = self.political_layer.__getitem__((tile_x,tile_y))
                    if political_tile_to_edit:
                        political_tile_to_edit.color = REVERSED_POLITICAL_ID_MAP.get(self.selected_country_id,0)
                        political_tile_to_edit.id_ = self.selected_country_id
                        print(f"set {tile_x,tile_y} to id {self.selected_country_id}, color {REVERSED_POLITICAL_ID_MAP.get(self.selected_country_id,0)}")

            else:
                if self.selected_icon_id or self.selected_icon_id == 0:
                    if self.selected_icon_id == 9:
                        if self.drawing_line_start == None:
                            self.drawing_line_start = (world_x,world_y)
                            self.on_notification_toast(f"starting line at {world_x,world_y}")
                        else:
                            self.drawing_line_end = (world_x,world_y)
                            self.icons['lines'].append((self.drawing_line_start, self.drawing_line_end))
                            self.on_notification_toast(f"made line at {self.drawing_line_start} . {self.drawing_line_end}")
                            self.drawing_line_start = None
                            self.drawing_line_end = None
                    else:
                        icon_path = str(ICON_ID_MAP.get(self.selected_icon_id))+".png"
                        generated_unique_id:int = random.randrange(1000,9999)
                        icon = Infocon(icon_path,1,world_x,world_y,0.0,self.selected_icon_id,"",0,0,icon_path,generated_unique_id,0)
                        self.info_scene.add_sprite("0",icon)
                        self.info_scene_list.append(icon)
                        self.icons["locations"].append({
                            "id": self.selected_icon_id,
                            "x": world_x,
                            "y": world_y,
                            "text": "",
                            "people_count": 0,
                            "angle_rot": 0,
                            "typename": icon_path,
                            "unique_id": generated_unique_id,
                            "country_id": 0
                        })
                        #self.selected_icon_id = None

                nearby_icon = self.find_icon_near(world_x, world_y, radius=10)
                nearby_line = self.find_line_near(world_x, world_y, radius=10)
                if nearby_icon:
                    self.selected_world_icon = nearby_icon
                    nearby_icon_dict = None
                    nearby_icon_dict_index = 0
                    for icon in self.icons['locations']:
                        if icon['unique_id'] == nearby_icon.unique_id:
                            nearby_icon_dict = icon
                            self.on_notification_toast(f"Found corresponding icon in dict. index;{nearby_icon_dict_index}")
                            break
                        else:
                            nearby_icon_dict_index+=1
                    self.icon_description.clear()
                    label = arcade.gui.UITextArea(
                        text=f"{nearby_icon.typename}\nPeople count: {nearby_icon.people_count}\n{nearby_icon.text}",
                        multiline=True,
                        width=320,
                        height=64
                    ).with_background(color=arcade.types.Color(10,10,10,255)).with_border(width=1,color=arcade.types.Color(30,30,30,255))
                    move_button_icon            = arcade.load_texture("icons/move_icon.png")
                    remove_button_icon          = arcade.load_texture("icons/remove_icon.png")
                    rotate_button_icon          = arcade.load_texture("icons/rotate_icon.png")
                    rotate_reset_button_icon    = arcade.load_texture("icons/rotate_reset_icon.png")
                    move_button = arcade.gui.UIFlatButton(text="", width=64, height=64)
                    move_button.add(
                        child=arcade.gui.UIImage(
                            texture=move_button_icon,
                            width =64,
                            height=64,
                        ),
                        anchor_x="center",
                        anchor_y="center"
                    )
                    
                    remove_button = arcade.gui.UIFlatButton(text="", width=64, height=64)
                    remove_button.add(
                        child=arcade.gui.UIImage(
                            texture=remove_button_icon,
                            width =64,
                            height=64,
                        ),
                        anchor_x="center",
                        anchor_y="center"
                    )
                    
                    rotate_button = arcade.gui.UIFlatButton(text="", width=64, height=64)
                    rotate_button.add(
                        child=arcade.gui.UIImage(
                            texture=rotate_button_icon,
                            width =64,
                            height=64,
                        ),
                        anchor_x="center",
                        anchor_y="center"
                    )
                    
                    rotate_reset_button = arcade.gui.UIFlatButton(text="", width=64, height=64)
                    rotate_reset_button.add(
                        child=arcade.gui.UIImage(
                            texture=rotate_reset_button_icon,
                            width =64,
                            height=64,
                        ),
                        anchor_x="center",
                        anchor_y="center"
                    )
                    
                    edit_text_button = arcade.gui.UIFlatButton(text="edit text",width=80,height=48)
                    @edit_text_button.event
                    def on_click(event: arcade.gui.UIOnClickEvent):
                        text_input = self.icon_description.add(
                            arcade.gui.UIInputText(
                                width=128,
                                height=32,
                                font_size=12,
                                border_color=arcade.uicolor.GRAY_CONCRETE,
                                border_width=2
                            ).with_background(color=arcade.types.Color(20,20,20,255))
                        )

                        @text_input.event("on_change")
                        def on_text_change(event: arcade.gui.UIOnChangeEvent):
                            nearby_icon.text = event.new_value
                            nearby_icon_dict['text'] = event.new_value
                    
                    edit_number_button = arcade.gui.UIFlatButton(text="edit people",width=80,height=48)
                    @edit_number_button.event
                    def on_click(event: arcade.gui.UIOnClickEvent):
                        text_input = self.icon_description.add(
                            arcade.gui.UIInputText(
                                width=128,
                                height=32,
                                font_size=12,
                                border_color=arcade.uicolor.GRAY_CONCRETE,
                                border_width=2
                            ).with_background(color=arcade.types.Color(20,20,20,255))
                        )

                        @text_input.event("on_change")
                        def on_text_change(event: arcade.gui.UIOnChangeEvent):
                            nearby_icon.people_count = event.new_value
                            nearby_icon_dict['people_count'] = event.new_value

                    edit_country_button = arcade.gui.UIFlatButton(text="edit country",width=80,height=48)
                    @edit_country_button.event
                    def on_click(event: arcade.gui.UIOnClickEvent):
                        text_input = self.icon_description.add(
                            arcade.gui.UIInputText(
                                width=128,
                                height=32,
                                font_size=12,
                                border_color=arcade.uicolor.GRAY_CONCRETE,
                                border_width=2
                            ).with_background(color=arcade.types.Color(20,20,20,255))
                        )

                        @edit_country_button.event("on_change")
                        def on_text_change(event: arcade.gui.UIOnChangeEvent):
                            nearby_icon.country_id = event.new_value
                            nearby_icon_dict['country_id'] = event.new_value

                    @rotate_button.event
                    def on_click(event: arcade.gui.UIOnClickEvent):
                        self.rotating_the_icon = not self.rotating_the_icon

                    @rotate_reset_button.event
                    def on_click(event: arcade.gui.UIOnClickEvent):
                        self.selected_world_icon.angle = 0
                        nearby_icon_dict['angle_rot'] = 0

                    @move_button.event
                    def on_click(event: arcade.gui.UIOnClickEvent):
                        self.moving_the_icon = True

                    @remove_button.event
                    def on_click(event: arcade.gui.UIOnClickEvent):
                        self.info_scene_list.remove(self.selected_world_icon)
                        abc = self.info_scene.get_sprite_list("0")
                        abc.remove(self.selected_world_icon)
                        self.icons['locations'].pop(nearby_icon_dict_index)
                        self.icon_description.clear()
                        self.on_notification_toast("Successfully removed icon.")

                        self.selected_world_icon = None

                    self.icon_description.add(label)
                    self.icon_description.add(move_button)
                    self.icon_description.add(remove_button)
                    self.icon_description.add(rotate_button)
                    self.icon_description.add(rotate_reset_button)
                    self.icon_description.add(edit_text_button)
                    self.icon_description.add(edit_number_button)
                    self.icon_description.add(edit_country_button)
                else:
                    if nearby_line:
                        index = 0
                        for line in self.icons['lines']:
                            if line[0][0] == nearby_line[0][0] and line[0][1] == nearby_line[0][1]:
                                #self.icons['lines'].pop(index)
                                self.selected_line = (nearby_line[0][0],nearby_line[0][1])
                                self.on_notification_toast(f"Found line at {round(nearby_line[0][0])} and {round(nearby_line[0][1])}")
                                break
                            else:
                                index += 1

                        self.icon_description.clear()
                        label = arcade.gui.UITextArea(
                            text=f"Line {round(nearby_line[0][0])} {round(nearby_line[0][1])}",
                            multiline=True,
                            width=128,
                            height=64
                        ).with_background(color=arcade.types.Color(10,10,10,255)).with_border(width=1,color=arcade.types.Color(30,30,30,255))
                        remove_button_icon = arcade.load_texture("icons/remove_icon.png")
                        remove_button = arcade.gui.UIFlatButton(text="", width=64, height=64)
                        remove_button.add(
                            child=arcade.gui.UIImage(
                                texture=remove_button_icon,
                                width =64,
                                height=64,
                            ),
                            anchor_x="center",
                            anchor_y="center"
                        )
                        
                        @remove_button.event
                        def on_click(event: arcade.gui.UIOnClickEvent):
                            self.icons['lines'].pop(index)
                            self.selected_line = None
                            self.icon_description.clear()
                            self.on_notification_toast("Successfully removed line.")

                        self.icon_description.add(label)
                        self.icon_description.add(remove_button)
                    else:
                        print("Found absolutely nothing in vicinity.") 
                        self.selected_world_icon = None
                        self.selected_line = None
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
            tile_x = round(world_x / 20)
            tile_y = round(world_y / 20)

            self.current_position_world = (world_x, world_y)

            if self.rotating_the_icon:
                try:
                    current_angle = math.atan2(world_x - self.selected_world_icon.position[0], world_y - self.selected_world_icon.position[1])
                    delta_angle = (((current_angle - self.previous_angle + math.pi) % (2 * math.pi)) - math.pi) * 100#???
                    self.selected_world_icon.angle += delta_angle
                    self.previous_angle = current_angle

                    index = 0
                    for icon in self.icons['locations']:
                        if icon['x'] == self.selected_world_icon.position[0] and icon['y'] == self.selected_world_icon.position[1]:
                            icon['angle_rot'] += delta_angle
                        else:
                            index+=1
                except:
                    self.on_notification_toast("Couldn't rotate [cannot find icon] ...", warn=True)

            if self.editing_mode == True:
                if self.camera.zoom >= 2.5:
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
                                    list_of_tiles[x_offset, y_offset] = self.lower_terrain_layer.__getitem__((round(x_ + 9.5), round(y_ + 9.5)))
                                    list_of_tile_positions.append((round(x_ + 9.5), round(y_ + 9.5)))
                                else:
                                    list_of_tiles[x_offset, y_offset] = None 
                            else:
                                list_of_tiles[x_offset, y_offset] = self.lower_terrain_layer.__getitem__((round(x_ + 9.5), round(y_ + 9.5)))
                                list_of_tile_positions.append((round(x_ + 9.5), round(y_ + 9.5)))

                    for x_ in range(self.editing_mode_size):
                        for y_ in range(self.editing_mode_size):
                            if not list_of_tiles[x_][y_] is None:
                                pixel_rgba = REVERSED_ID_MAP.get(self.selected_lower_id,(0,0,0)) + (255,)
                                list_of_tiles[x_][y_].color = pixel_rgba
                                list_of_tiles[x_][y_].id_ = self.selected_lower_id
                            else:
                                print(f"no tiles returned to selection ...")
                
                elif self.camera.zoom < 2.5:
                    political_tile_to_edit = self.political_layer.__getitem__((tile_x,tile_y))
                    if political_tile_to_edit:
                        political_tile_to_edit.color = REVERSED_POLITICAL_ID_MAP.get(self.selected_country_id,0)
                        political_tile_to_edit.id_ = self.selected_country_id
                        print(f"set {tile_x,tile_y} to id {self.selected_country_id}, color {REVERSED_POLITICAL_ID_MAP.get(self.selected_country_id,0)}")

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
            #self.moving_the_icon = False

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
        self.last_interacted_tile = self.upper_terrain_layer.__getitem__((tile_x, tile_y))

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
    