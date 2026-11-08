import math
import pygame
from src.game import content
from src.ui.text import draw_text
from src.ui.imageload import load


_icon_cache = {}
_ITEM_TEX = {
    content.GRASS: 'grass_top.png', content.DIRT: 'dirt.png',
    content.STONE: 'stone.png', content.LOG: 'log_top.png',
    content.LEAVES: 'leaves.png', content.SAND: 'sand.png',
    content.CRAFTING_TABLE: 'craft_table_top.png', content.PLANKS: 'planks.png',
    content.ITEM_STICK: 'item_stick.png',
    content.ITEM_WOOD_PICKAXE: 'item_pickaxe.png',
    content.ITEM_WOOD_AXE: 'item_axe.png',
    content.ITEM_WOOD_SHOVEL: 'item_shovel.png',
    content.ITEM_WOOD_SWORD: 'item_sword.png',
}


def get_icon(item, size):
    key = (item, size)
    if key in _icon_cache:
        return _icon_cache[key]
    tex = _ITEM_TEX.get(item)
    if not tex:
        return None
    try:
        img = load(tex, (size, size))
        _icon_cache[key] = img
        return img
    except Exception:
        return None


def draw_crosshair(surf, W, H):
    cx, cy = W // 2, H // 2
    pygame.draw.line(surf, (255, 255, 255), (cx - 8, cy), (cx + 8, cy), 2)
    pygame.draw.line(surf, (255, 255, 255), (cx, cy - 8), (cx, cy + 8), 2)


def draw_hotbar(surf, inv, W, H):
    ss = 44
    total = ss * 9
    x0 = (W - total) // 2
    y0 = H - ss - 8
    pygame.draw.rect(surf, (30, 30, 30), (x0 - 2, y0 - 2, total + 4, ss + 4))
    for i in range(9):
        sx = x0 + i * ss
        pygame.draw.rect(surf, (100, 100, 100), (sx + 2, y0 + 2, ss - 4, ss - 4))
        pygame.draw.rect(surf, (40, 40, 40), (sx + 2, y0 + 2, ss - 4, ss - 4), 1)
        if i == inv.selected:
            pygame.draw.rect(surf, (255, 255, 255), (sx, y0, ss, ss), 2)
        slot = inv.slots[i]
        if slot:
            icon = get_icon(slot[0], ss - 12)
            if icon:
                surf.blit(icon, (sx + 6, y0 + 6))
            if slot[1] > 1:
                draw_text(surf, str(slot[1]), sx + ss - 4, y0 + ss - 16,
                          size=8, scale=1, right=True)

    item = inv.selected_item()
    if item:
        name = content.ITEM_NAMES.get(item) or content.BLOCK_NAMES.get(item, '')
        if name:
            draw_text(surf, name, W // 2, y0 - 26, size=9, scale=2, center=True)


def draw_hand(surf, player, inv, break_progress):
    W, H = surf.get_size()
    bx = W - 130
    by = H - 210
    if player.is_walking:
        bx += int(math.sin(player.walk_time) * 8)
        by += int(abs(math.cos(player.walk_time)) * 8)
    if break_progress > 0:
        phase = (break_progress * 3) % 1.0
        bx -= int(math.sin(phase * math.pi) * 30)
        by += int(math.cos(phase * math.pi) * 20)

    # Arm
    aw, ah = 90, 180
    pygame.draw.rect(surf, (215, 175, 135), (bx, by, aw, ah))
    pygame.draw.rect(surf, (160, 120, 85), (bx, by, aw, ah), 3)
    # Fist highlight
    pygame.draw.rect(surf, (235, 195, 155), (bx + 6, by + 6, aw - 12, 40))
    # Sleeve (blue)
    pygame.draw.rect(surf, (55, 85, 155), (bx, by + ah - 50, aw, 50))
    pygame.draw.rect(surf, (30, 55, 115), (bx, by + ah - 50, aw, 50), 2)

    item = inv.selected_item()
    if item:
        icon = get_icon(item, 70)
        if icon:
            surf.blit(icon, (bx - 20, by + 20))


def draw_fps(surf, fps):
    draw_text(surf, f"FPS: {fps}", 10, 10, size=8, scale=2)
