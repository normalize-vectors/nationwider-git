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