import math
import pygame
from src.game.content import (SOLID, WATER, GRASS, DIRT, STONE, LOG, LEAVES,
                               SAND, CRAFTING_TABLE, PLANKS, BLOCK_COLORS)

SKY_TOP = (100, 170, 220)
SKY_BOTTOM = (190, 225, 245)
_sky_cache = None


def _shade(c, f):
    return (max(0, min(255, int(c[0]*f))), max(0, min(255, int(c[1]*f))),
            max(0, min(255, int(c[2]*f))))


def _project_y(rel_h, d_perp, pitch, focal, half_h):
    cos_p, sin_p = math.cos(pitch), math.sin(pitch)
    y_cam = rel_h * cos_p - d_perp * sin_p
    z_cam = rel_h * sin_p + d_perp * cos_p
    if z_cam < 0.1:
        return None
    return half_h - (y_cam / z_cam) * focal


def _sky(surf):
    global _sky_cache
    W, H = surf.get_size()
    if _sky_cache is None or _sky_cache.get_size() != (W, H):
        _sky_cache = pygame.Surface((W, H))
        for y in range(H):
            t = y / H
            c = tuple(int(SKY_TOP[i]*(1-t) + SKY_BOTTOM[i]*t) for i in range(3))
            pygame.draw.line(_sky_cache, c, (0, y), (W, y))
    surf.blit(_sky_cache, (0, 0))


def render_world(surf, camera, world):
    W, H = surf.get_size()
    half_w, half_h = W // 2, H // 2
    focal = half_w / math.tan(math.radians(75) / 2)
    _sky(surf)

    eye_y, cam_x, cam_z = camera.eye_y, camera.x, camera.z
    max_steps = 20

    for x in range(W):
        angle = math.atan((x - half_w) / focal)
        wa = camera.yaw + angle
        dx, dz = math.sin(wa), math.cos(wa)
        inv_cos = focal / math.sqrt(focal*focal + (x - half_w)**2)

        map_x, map_z = int(cam_x // 1), int(cam_z // 1)
        INF = 1e30
        ddx = abs(1/dx) if dx != 0 else INF
        ddz = abs(1/dz) if dz != 0 else INF
        if dx < 0:
            step_x, sx = -1, (cam_x - map_x) * ddx
        else:
            step_x, sx = 1, (map_x + 1 - cam_x) * ddx
        if dz < 0:
            step_z, sz = -1, (cam_z - map_z) * ddz
        else:
            step_z, sz = 1, (map_z + 1 - cam_z) * ddz

        hits = []
        for _ in range(max_steps):
            if sx < sz:
                d = sx; sx += ddx; map_x += step_x; side = 0
                frac = (cam_z + dz * d) - math.floor(cam_z + dz * d)
            else:
                d = sz; sz += ddz; map_z += step_z; side = 1
                frac = (cam_x + dx * d) - math.floor(cam_x + dx * d)
            if d > 22:
                break
            dp = d * inv_cos
            for by, block in world.solid_column(map_x, map_z):
                st = _project_y((by+1) - eye_y, dp, camera.pitch, focal, half_h)
                sb = _project_y(by - eye_y, dp, camera.pitch, focal, half_h)
                if st is None or sb is None:
                    continue
                if st > sb: st, sb = sb, st
                hits.append((dp, block, st, sb, side, frac))

        hits.sort(key=lambda h: -h[0])
        for dp, block, st, sb, side, frac in hits:
            y0 = max(0, int(st))
            y1 = min(H - 1, int(sb))
            if y0 > y1:
                continue
            if block == WATER:
                pygame.draw.rect(surf, (60, 120, 210), (x, y0, 1, y1-y0+1))
                continue
            sf = 0.8 if side == 0 else 0.7
            base = BLOCK_COLORS.get(block, (255, 0, 255))
            u = int(frac * 16) & 15
            noise = ((u * 73 + (map_x if side == 0 else map_z) * 37) % 7) - 3
            shaded = _shade((base[0]+noise*3, base[1]+noise*3, base[2]+noise*3), sf)

            if block == GRASS and side in (0, 1) and (y1-y0) > 3:
                gh = int((y1 - y0) * 3 / 16)
                green_end = min(y1, y0 + gh)
                pygame.draw.rect(surf, _shade((95, 159, 53), sf),
                                 (x, y0, 1, green_end - y0 + 1))
                if y1 > green_end:
                    pygame.draw.rect(surf, _shade((134, 96, 67), sf),
                                     (x, green_end + 1, 1, y1 - green_end))
            else:
                pygame.draw.rect(surf, shaded, (x, y0, 1, y1 - y0 + 1))


def render_selection(surf, camera, block_pos):
    W, H = surf.get_size()
    half_w, half_h = W // 2, H // 2
    focal = half_w / math.tan(math.radians(75) / 2)
    x0, y0, z0 = block_pos
    corners = [(x0, y0, z0), (x0+1, y0, z0), (x0+1, y0, z0+1), (x0, y0, z0+1),
               (x0, y0+1, z0), (x0+1, y0+1, z0), (x0+1, y0+1, z0+1), (x0, y0+1, z0+1)]
    proj = []
    for cx, cy, cz in corners:
        rx, ry, rz = cx - camera.x, cy - camera.eye_y, cz - camera.z
        cos_y, sin_y = math.cos(-camera.yaw), math.sin(-camera.yaw)
        x1 = rx*cos_y - rz*sin_y
        z1 = rx*sin_y + rz*cos_y
        cos_p, sin_p = math.cos(-camera.pitch), math.sin(-camera.pitch)
        yy = ry*cos_p - z1*sin_p
        zz = ry*sin_p + z1*cos_p
        if zz < 0.1:
            return
        proj.append((int(half_w + (x1/zz)*focal), int(half_h - (yy/zz)*focal)))
    for a, b in [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),
                 (0,4),(1,5),(2,6),(3,7)]:
        pygame.draw.line(surf, (0, 0, 0), proj[a], proj[b], 1)
