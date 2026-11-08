import math
import random
import zlib
import base64
from src.game.content import (AIR, GRASS, DIRT, STONE, LOG, LEAVES,
                               WATER, SAND, SOLID)

SEA_LEVEL = 28
SIZE_X = 80
SIZE_Y = 80
SIZE_Z = 80


class World:
    def __init__(self, data):
        self.seed = data.get('seed', 0)
        self.size_x, self.size_y, self.size_z = SIZE_X, SIZE_Y, SIZE_Z
        world_data = data.get('world', {})
        blocks_ser = world_data.get('blocks')
        if blocks_ser:
            self._deserialize(blocks_ser)
        else:
            self._generate()
        self._rebuild_all()

    def _generate(self):
        rng = random.Random(self.seed)
        p = [rng.random() * 6.283 for _ in range(4)]
        heights = [[0] * self.size_z for _ in range(self.size_x)]
        for x in range(self.size_x):
            for z in range(self.size_z):
                h = int(28 + 8 * math.sin(x * 0.12 + p[0]) * math.cos(z * 0.14 + p[1])
                        + 4 * math.sin(x * 0.28 + p[2]) * math.cos(z * 0.31 + p[3])
                        + rng.randint(-1, 1))
                heights[x][z] = max(8, min(self.size_y - 12, h))

        self.blocks = [[[AIR] * self.size_z for _ in range(self.size_y)]
                       for _ in range(self.size_x)]
        for x in range(self.size_x):
            for z in range(self.size_z):
                h = heights[x][z]
                for y in range(0, max(0, h - 4)):
                    self.blocks[x][y][z] = STONE
                for y in range(max(0, h - 4), h):
                    self.blocks[x][y][z] = DIRT
                self.blocks[x][h][z] = SAND if h < SEA_LEVEL + 1 else GRASS
                if h < SEA_LEVEL:
                    for y in range(h + 1, SEA_LEVEL + 1):
                        self.blocks[x][y][z] = WATER

        placed = set()
        for _ in range(200):
            if len(placed) >= 25:
                break
            tx = rng.randint(3, self.size_x - 4)
            tz = rng.randint(3, self.size_z - 4)
            if (tx, tz) in placed:
                continue
            th = heights[tx][tz]
            if self.blocks[tx][th][tz] != GRASS:
                continue
            ok = all(abs(heights[tx + dx][tz + dz] - th) <= 1
                     for dx in (-1, 0, 1) for dz in (-1, 0, 1))
            if not ok:
                continue
            trunk_h = rng.randint(4, 6)
            for ty in range(th + 1, min(self.size_y, th + 1 + trunk_h)):
                self.blocks[tx][ty][tz] = LOG
            top = th + trunk_h
            for dx in range(-2, 3):
                for dz in range(-2, 3):
                    for dy in range(-2, 2):
                        if dx == 0 and dz == 0 and dy < 1:
                            continue
                        if abs(dx) == 2 and abs(dz) == 2:
                            continue
                        lx, ly, lz = tx + dx, top + dy, tz + dz
                        if 0 <= lx < self.size_x and 0 <= ly < self.size_y and 0 <= lz < self.size_z:
                            if self.blocks[lx][ly][lz] == AIR:
                                self.blocks[lx][ly][lz] = LEAVES
            placed.add((tx, tz))

    def get_block(self, x, y, z):
        if 0 <= x < self.size_x and 0 <= y < self.size_y and 0 <= z < self.size_z:
            return self.blocks[x][y][z]
        return AIR

    def set_block(self, x, y, z, block):
        if 0 <= x < self.size_x and 0 <= y < self.size_y and 0 <= z < self.size_z:
            self.blocks[x][y][z] = block
            self._rebuild_column(x, z)

    def _rebuild_all(self):
        self._solid = [[[] for _ in range(self.size_z)] for _ in range(self.size_x)]
        for x in range(self.size_x):
            for z in range(self.size_z):
                self._rebuild_column(x, z)

    def _rebuild_column(self, x, z):
        col = []
        for y in range(self.size_y):
            b = self.blocks[x][y][z]
            if b in SOLID or b == WATER:
                col.append((y, b))
        self._solid[x][z] = col

    def solid_column(self, x, z):
        if 0 <= x < self.size_x and 0 <= z < self.size_z:
            return self._solid[x][z]
        return []

    def surface_height(self, x, z):
        for y, b in reversed(self.solid_column(x, z)):
            if b in SOLID:
                return y
        return 0

    def serialize(self):
        data = bytearray()
        for x in range(self.size_x):
            for y in range(self.size_y):
                data.extend(self.blocks[x][y])
        return base64.b64encode(zlib.compress(bytes(data), 6)).decode('ascii')

    def _deserialize(self, s):
        raw = zlib.decompress(base64.b64decode(s))
        self.blocks = [[[AIR] * self.size_z for _ in range(self.size_y)]
                       for _ in range(self.size_x)]
        i = 0
        for x in range(self.size_x):
            for y in range(self.size_y):
                for z in range(self.size_z):
                    self.blocks[x][y][z] = raw[i]
                    i += 1
