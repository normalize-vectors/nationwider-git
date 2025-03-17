        # tile_size_pair = (20, 20)
        # for x in range(img_width):
        #     column = np.zeros(img_height,dtype=object)
        #     for y in range(img_height):
        #         pixel_rgb = tuple(pixels[x,y])
        #         id_value = ID_MAP.get(pixel_rgb, None)
                
        #         if not id_value:
        #             print(f"ERR unknown tile color : {pixel_rgb}")
        #             continue

        #         pixel_rgba = pixel_rgb + (255,)
        #         world_x = x * 20
        #         world_y = y * 20
                
        #         if pixel_rgb == (0,0,127):
        #             tile = Tile(*tile_size_pair, world_x, world_y, (0,0,0,0), id_value)
        #             political_tile = Tile(*tile_size_pair, world_x, world_y, (56, 56, 56, 100), 30)
        #         else:
        #             tile = Tile(*tile_size_pair, world_x, world_y, pixel_rgba, id_value)
        #             political_tile = Tile(*tile_size_pair, world_x, world_y, (56, 56, 56, 255), 30)

        #         self.terrain_scene.add_sprite("1",tile)
        #         self.political_scene.add_sprite("0", political_tile)
        #         column[y] = tile

        #     self.high_terrain_layer.grid[x] = column


        # image = Image.open("map_image_data/biomemap.png")
        # pixels = np.array(image).tolist()
        # id_grid = np.zeros((600,300),dtype=np.uint8)
        # id_grid_political = np.zeros((600,300),dtype=np.uint8)
        # small_id_grid = np.full((12000,6000),32,dtype=np.uint8)
        # for x in range(600):
        #     biome_column = np.zeros(300,dtype=object)
        #     politic_column = np.zeros(300,dtype=object)
        #     if x % 50 == 0:
        #         print(f"Progress: {x} rows generated...")
        #     for y in range(300):
        #         pixel_rgb = pixels[y][x]
        #         pixel_rgba = (pixel_rgb[0],pixel_rgb[1],pixel_rgb[2],255)
        #         id_value = ID_MAP.get((pixel_rgb[0],pixel_rgb[1],pixel_rgb[2]),0)
        #         world_x = x * 20
        #         world_y = y * 20

        #         if pixel_rgba == (0,0,127,255):
        #             tile = Tile(20, 20, world_x, world_y, (0,0,0,0), id_value)
        #             political_tile = Tile(20, 20, world_x, world_y, (56, 56, 56, 100), 30)
        #             id_grid_political[x][y] = 29
        #         else:
        #             tile = Tile(20, 20, world_x, world_y, pixel_rgba, id_value)
        #             political_tile = Tile(20, 20, world_x, world_y, (56, 56, 56, 255), 30)
        #             id_grid_political[x][y] = 30

        #         self.terrain_scene.add_sprite("1",tile)
        #         self.political_scene.add_sprite("0", political_tile)
        #         biome_column[y] = tile
        #         politic_column[y] = political_tile
        #         id_grid[x][y] = id_value

        #     self.high_terrain_layer.grid[x] = biome_column
        #     self.political_layer.grid[x] = politic_column

        


        # image_path = "map_image_data/biomemap_south.png"
        # image = Image.open(image_path).convert("RGB")

        # image_array = np.array(image)

        # def rgb_to_id(rgb):
        #     return ID_MAP.get(tuple(rgb), 255) 

        # self.s_loaded_id_grid = np.apply_along_axis(rgb_to_id, axis=-1, arr=image_array)



        # if self.editing_mode == False:
        #     if self.moving_the_icon == False:
        #         if self.last_pressed_world:
        #             if self.current_position_world:
        #                 # selection rectangle coordinates
        #                 left = min(self.last_pressed_world[0], self.current_position_world[0])
        #                 right = max(self.last_pressed_world[0], self.current_position_world[0])
        #                 bottom = min(self.last_pressed_world[1], self.current_position_world[1])
        #                 top = max(self.last_pressed_world[1], self.current_position_world[1])

        #                 arcade.draw_lrbt_rectangle_outline(left, right, bottom, top, arcade.color.ORIOLES_ORANGE, self.selection_rectangle_size)
        #                 # ^ drawing the selection



        # if self.current_position_world:
        #     nearby_icon = self.find_icon_near(self.current_position_world[0], self.current_position_world[1], radius=32)
        #     if nearby_icon:
        #         if self.current_position_world:
        #             #arcade.draw_text(nearby_icon.typename,nearby_icon.position[0],nearby_icon.position[1]+16,arcade.color.WHITE,9,width=64,multiline=True,anchor_x="center",)
        #             text = arcade.Text(nearby_icon.typename,nearby_icon.position[0],nearby_icon.position[1]+16,arcade.color.WHITE,12,64,"center","calibri",False,False,"center","top",True,0,None,None,0)
        #             text.draw()