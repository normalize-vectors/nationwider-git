import numpy as np
import threading
import queue
from arcade import SpriteSolidColor, color as cl

class Tile(SpriteSolidColor):
    def __init__(self, width, height, x, y, color, id_):
        super().__init__(width, height, x, y, cl.WHITE)
        self.color = color
        self.id_ = id_

class ChunkFetcher:
    def __init__(self, id_grid, tile_grid, chunk_size=(20, 20)):
        self.grid = id_grid
        self.chunk_size = chunk_size
        self.request_queue = queue.Queue()
        self.result_dict = {}
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self._process_requests, daemon=True)
        self.thread.start()
        self.tile_grid = tile_grid
    
    def _process_requests(self):
        while True:
            chunk_loc = self.request_queue.get()
            if chunk_loc is None:
                break  # Exit condition
            chunk_data = self._fetch_chunk(chunk_loc)
            with self.lock:
                self.result_dict[chunk_loc] = chunk_data
    
    def _fetch_chunk(self, chunk_loc):
        x, y = chunk_loc
        returnable_grid = []
        for x_ in range(self.chunk_size[0]):
            for y_ in range(self.chunk_size[1]):

        x_start, y_start = x * self.chunk_size[0], y * self.chunk_size[1]
        x_end, y_end = x_start + self.chunk_size[0], y_start + self.chunk_size[1]
        return self.grid[x_start:x_end, y_start:y_end]
    
    def request_chunk(self, chunk_loc):
        if chunk_loc not in self.result_dict:
            self.request_queue.put(chunk_loc)
    
    def get_chunk(self, chunk_loc):
        with self.lock:
            return self.result_dict.get(chunk_loc, None)
    
    def stop(self):
        self.request_queue.put(None)
        self.thread.join()

if __name__ == "__main__":
    # Example Usage
    grid = np.zeros((600,300),dtype=np.uint8)
    fetcher = ChunkFetcher(grid)

    # Request some chunks
    fetcher.request_chunk((599,299))

    # Wait for some time for the thread to process
    import time
    time.sleep(1)  # Allow the worker to process

    # Retrieve chunks
    chunk1 = fetcher.get_chunk((599,299))

    print(chunk1)

    fetcher.stop()