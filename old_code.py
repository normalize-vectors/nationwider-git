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