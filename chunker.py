import json
import numpy as np

class Manager():
    def __init__(self, filename: str):
        self.filename = filename

        self.loaded_world_data = None

    def load_world(self):
        """Loads the all the chunks of the world."""
        with open(self.filename, "r") as file_:
            data = json.loads(file_.read())
            self.loaded_world_data = {
                tuple(chunk["position"]): chunk for chunk in data["chunks"]
            }

    def fetch_chunk(self, chunk_position: tuple):
        """Fetches the requested chunk."""
        chunk = self.loaded_world_data.get(chunk_position)
        if chunk is None:
            return None
        self.chunk_data = np.array(chunk["tiles"])
        return self.chunk_data
    
    def save_chunk_at(self, chunk_position: tuple, new_tiles):
        """Saves tiles to chunk position."""
        if isinstance(new_tiles, np.ndarray):
            new_tiles = new_tiles.tolist()

        self.loaded_world_data[chunk_position] = {
            "position": list(chunk_position),
            "tiles": new_tiles
        }

        data_to_save = {"chunks": list(self.loaded_world_data.values())}
        with open(self.filename, "w") as file_:
            json.dump(data_to_save, file_)

    def generate_world(self):
        """Dummy operation to fill each chunk with data"""
        chunk = np.zeros((20,20))
        for x in range(600):
            if x % 50 == 0:
                print(f"progress ... {x}")
            for y in range(300):
                new_tiles = chunk.tolist()
                self.loaded_world_data[(x,y)] = {
                    "position": list((x,y)),
                    "tiles": new_tiles
                }
        print("Data generated ...")
        data_to_save = {"chunks": list(self.loaded_world_data.values())}
        file_  = open(self.filename, "w")
        json.dump(data_to_save, file_)
        file_.close()

        print("Generated world ...")


if __name__ == "__main__":
    import time
    manager = Manager()

    start_time = time.time()
    manager.load_world()
    print(f"time taken for loading world: {round(time.time() - start_time, 4)}")
    #manager.generate_world()

    start_time = time.time()
    manager.fetch_chunk((0,0))
    print(f"time taken for fetching chunk: {round(time.time() - start_time, 4)}")