import time
import numpy as np
import nation_utils as na

political_layer        = na.GridLayer((600,300)   ,20)
upper_terrain_layer    = na.GridLayer((600,300)   ,20)
lower_terrain_layer    = na.GridLayer((12000,6000),1 )

s_political_layer      = na.GridLayer((600,300)   ,20)
s_upper_terrain_layer  = na.GridLayer((600,300)   ,20)
icons = {
    'locations': [],
    'lines': []
}

loaded_data = np.load('local_data/default_mapdata.npz',allow_pickle=True)
loaded_a_data                   = loaded_data['a']
upper_terrain_layer.grid[:]= loaded_a_data

loaded_b_data                   = loaded_data['b']
political_layer.grid[:]    = loaded_b_data

loaded_c_data                   = loaded_data['c']
lower_terrain_layer.grid[:]= loaded_c_data

loaded_a_s_data                 = loaded_data['a_s']
s_upper_terrain_layer.grid[:]=loaded_a_s_data

loaded_b_s_data                 = loaded_data['b_s']
s_political_layer.grid[:]  = loaded_b_s_data

icons_array                     = loaded_data['cc']
icons = icons_array.item()

# Convert to (y, x) format
upper_terrain_layer.grid = upper_terrain_layer.grid.T
political_layer.grid = political_layer.grid.T
lower_terrain_layer.grid = lower_terrain_layer.grid.T
s_upper_terrain_layer.grid = s_upper_terrain_layer.grid.T
s_political_layer.grid = s_political_layer.grid.T

a_grid = np.empty((600,300),dtype=np.uint8)
a_grid = np.empty((600,300),dtype=np.uint8)
c_grid = np.empty((12000, 6000), dtype=np.uint8)

def extract_id(cell):
    return cell.id_ if isinstance(cell, na.Tile) else cell

def extract_country_id(cell):
    return cell.id_ if isinstance(cell, na.Tile) else cell

extract_attribute_biome = np.vectorize(extract_id, otypes=[np.uint8])
extract_attribute_country = np.vectorize(extract_country_id, otypes=[np.uint8])
a_grid = extract_attribute_biome(upper_terrain_layer.grid)
b_grid = extract_attribute_country(political_layer.grid)
c_grid = extract_attribute_biome(lower_terrain_layer.grid)

a_s_grid = extract_attribute_biome(s_upper_terrain_layer.grid)
b_s_grid = extract_attribute_country(s_political_layer.grid)
np.savez_compressed(f"local_data/converted_{time.localtime().tm_year}_{time.localtime().tm_mon}_{time.localtime().tm_mday}_{time.localtime().tm_hour}_{time.localtime().tm_min}_{time.localtime().tm_sec}.npz",
                    a=a_grid,
                    b=b_grid,
                    c=c_grid,
                    a_s=a_s_grid,
                    b_s=b_s_grid,
                    cc=np.array(icons)
                    )