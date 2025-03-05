import sqlite3
import json
import numpy as np

class Manager:
    def __init__(self, db_filename="chunks.db", tile_count: int = 1, map_size: tuple = (0, 0)):
        """Initialize the SQLite database."""
        self.db_filename = db_filename
        self.tile_count = tile_count
        self.map_size = map_size
        self._setup_db()

        master_conn = sqlite3.connect(self.db_filename, check_same_thread=False)
        master_conn.execute("PRAGMA journam_mode=WAL;")
        self.master_cursor = master_conn.cursor()

    def _get_connection(self):
        """Returns a new SQLite connection for safe multithreading."""
        conn = sqlite3.connect(self.db_filename, check_same_thread=False)
        conn.execute("PRAGMA journal_mode=WAL;")  # Speeds up writes
        return conn

    def _setup_db(self):
        """Creates tables for chunks and metadata."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # chunks
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chunks (
                position TEXT PRIMARY KEY,
                tiles TEXT
            )
        """)
        
        # metadata
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)

        conn.commit()
        conn.close()

    def set_map_size(self, width, height):
        """Stores map size in the metadata table."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT OR REPLACE INTO metadata VALUES ('width', ?)", (str(width),))
        cursor.execute("INSERT OR REPLACE INTO metadata VALUES ('height', ?)", (str(height),))
        conn.commit()
        conn.close()

    def get_map_size(self):
        """Retrieves map size from metadata table."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT value FROM metadata WHERE key='width'")
        width_result = cursor.fetchone()
        width = int(width_result[0]) if width_result else None

        cursor.execute("SELECT value FROM metadata WHERE key='height'")
        height_result = cursor.fetchone()
        height = int(height_result[0]) if height_result else None

        conn.close()
        return width, height

    def insert_chunk(self, chunk_position, tiles):
        """Inserts or updates a chunk in the database."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT OR REPLACE INTO chunks VALUES (?, ?)",
                       (json.dumps(chunk_position), json.dumps(tiles)))
        
        conn.commit()
        conn.close()

    def insert_chunk_masterthread(self, chunk_position, tiles):
        self.master_cursor.execute("INSERT OR REPLACE INTO chunks VALUES (?, ?)",
                       (json.dumps(chunk_position), json.dumps(tiles)))

    def fetch_chunk(self, chunk_position):
        """Fetches a chunk from the database."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT tiles FROM chunks WHERE position=?", (json.dumps(chunk_position),))
        result = cursor.fetchone()
        
        conn.close()

        if result:
            return np.array(json.loads(result[0]))
        return None
    
    def fetch_chunk_masterthread(self, chunk_position):
        self.master_cursor.execute("SELECT tiles FROM chunks WHERE position=?", (json.dumps(chunk_position),))
        result = self.master_cursor.fetchone()

        if result:
            return np.array(json.loads(result[0]))
        return None

    def generate_world(self):
        """Populates the database with example chunks."""
        conn = self._get_connection()
        cursor = conn.cursor()

        chunk = json.dumps(np.zeros((self.tile_count, self.tile_count), dtype=int).tolist())
        horizontal_size, vertical_size = self.map_size

        for x in range(horizontal_size):
            if x % 10 == 0:
                print(f"Progress: {x} rows generated...")

            for y in range(vertical_size):
                cursor.execute("INSERT OR REPLACE INTO chunks VALUES (?, ?)",
                               (json.dumps((x, y)), chunk))

        conn.commit()
        conn.close()
        print("World generation complete!")

    def convert_world(self, grid, width, height):
        conn = self._get_connection()
        cursor = conn.cursor()

        for x in range(width):
            if x % 10 == 0:
                print(f"Progress: {x} rows converted...")
            for y in range(height):
                tile = grid.__getitem__((x,y))
                tiles = json.dumps([tile.id_])

                cursor.execute("INSERT OR REPLACE INTO chunks VALUES (?, ?)",
                               (json.dumps((x, y)), tiles))

        conn.commit()
        conn.close()
        print("World conversion complete!")

if __name__ == "__main__":
    import time

    manager = Manager("savedata_lz4/upper_chunks.db", tile_count=1, map_size=(600, 300))

    # Uncomment to generate the world (only needed once)
    #manager.convert_world()

    # Fetching a chunk
    start_time = time.time()
    chunk_data = manager.fetch_chunk((599, 299))
    print(f"Time taken for fetching chunk: {round(time.time() - start_time, 4)} sec")
    
    if chunk_data is not None:
        print(f"Chunk fetched successfully!\n {chunk_data}")
    else:
        print("Chunk not found!")
