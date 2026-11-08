import math
from src.game.content import SOLID


def pick_block(eye, direction, world, max_dist=5.0):
    ox, oy, oz = eye
    dx, dy, dz = direction
    map_x, map_y, map_z = int(math.floor(ox)), int(math.floor(oy)), int(math.floor(oz))
    step_x = 1 if dx >= 0 else -1
    step_y = 1 if dy >= 0 else -1
    step_z = 1 if dz >= 0 else -1
    INF = 1e30
    tdx = abs(1/dx) if dx != 0 else INF
    tdy = abs(1/dy) if dy != 0 else INF
    tdz = abs(1/dz) if dz != 0 else INF
    tmx = ((map_x + 1 - ox) if dx >= 0 else (ox - map_x)) * tdx if dx != 0 else INF
    tmy = ((map_y + 1 - oy) if dy >= 0 else (oy - map_y)) * tdy if dy != 0 else INF
    tmz = ((map_z + 1 - oz) if dz >= 0 else (oz - map_z)) * tdz if dz != 0 else INF
    side = 0
    for _ in range(80):
        block = world.get_block(map_x, map_y, map_z)
        if block in SOLID:
            if side == 0:
                adj = (map_x - step_x, map_y, map_z)
            elif side == 1:
                adj = (map_x, map_y - step_y, map_z)
            else:
                adj = (map_x, map_y, map_z - step_z)
            return {'block_pos': (map_x, map_y, map_z), 'adjacent': adj, 'block': block}
        if tmx < tmy and tmx < tmz:
            if tmx > max_dist: return None
            map_x += step_x; tmx += tdx; side = 0
        elif tmy < tmz:
            if tmy > max_dist: return None
            map_y += step_y; tmy += tdy; side = 1
        else:
            if tmz > max_dist: return None
            map_z += step_z; tmz += tdz; side = 2
    return None
