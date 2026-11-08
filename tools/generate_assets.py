import os
import random
import struct
import pygame

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'textures', 'menu')
BLOCKS_OUT = os.path.join(ROOT, 'assets', 'textures', 'blocks')
ITEMS_OUT = os.path.join(ROOT, 'assets', 'textures', 'items')


def _noise(w, h, base, var):
    s = pygame.Surface((w, h))
    for x in range(w):
        for y in range(h):
            r = max(0, min(255, base[0] + random.randint(-var, var)))
            g = max(0, min(255, base[1] + random.randint(-var, var)))
            b = max(0, min(255, base[2] + random.randint(-var, var)))
            s.set_at((x, y), (r, g, b))
    return s


def _save(s, path):
    pygame.image.save(s, path)


# ===== UI (как было) =====
def make_ui_assets():
    s = _noise(16, 16, (134, 96, 67), 12)
    for _ in range(10):
        s.set_at((random.randint(0, 15), random.randint(0, 15)), (85, 55, 35))
    _save(s, os.path.join(OUT, 'dirt.png'))
    _save(_noise(16, 16, (128, 128, 128), 15), os.path.join(OUT, 'stone.png'))
    _save(_noise(16, 16, (95, 159, 53), 22), os.path.join(OUT, 'grass_top.png'))

    def btn(name, base, disabled=False):
        w, h = 200, 40
        s = pygame.Surface((w, h)); s.fill(base)
        if not disabled:
            hl = tuple(min(255, c + 55) for c in base)
            sh = tuple(max(0, c - 55) for c in base)
            pygame.draw.line(s, hl, (0, 0), (w-1, 0))
            pygame.draw.line(s, hl, (0, 0), (0, h-1))
            pygame.draw.line(s, sh, (0, h-1), (w-1, h-1))
            pygame.draw.line(s, sh, (w-1, 0), (w-1, h-1))
        pygame.draw.rect(s, (0, 0, 0), (0, 0, w, h), 1)
        _save(s, os.path.join(OUT, name))

    btn('button.png', (110, 110, 110))
    btn('button_hover.png', (130, 140, 200))
    btn('button_disabled.png', (70, 70, 70), True)

    # slider
    s = pygame.Surface((200, 20)); s.fill((35, 35, 35))
    pygame.draw.rect(s, (0, 0, 0), (0, 0, 200, 20), 1)
    pygame.draw.line(s, (65, 65, 65), (1, 1), (198, 1))
    _save(s, os.path.join(OUT, 'slider_track.png'))
    s = pygame.Surface((12, 24)); s.fill((180, 180, 180))
    pygame.draw.line(s, (220, 220, 220), (1, 1), (10, 1))
    pygame.draw.rect(s, (0, 0, 0), (0, 0, 12, 24), 1)
    _save(s, os.path.join(OUT, 'slider_handle.png'))

    # frame
    w, h = 500, 420
    s = pygame.Surface((w, h)); s.fill((198, 198, 198))
    pygame.draw.rect(s, (0, 0, 0), (0, 0, w, h), 2)
    pygame.draw.rect(s, (85, 85, 85), (2, 2, w-4, h-4), 2)
    pygame.draw.rect(s, (255, 255, 255), (4, 4, w-8, h-8), 1)
    pygame.draw.rect(s, (110, 110, 110), (5, 5, w-10, h-10))
    for _ in range(120):
        s.set_at((random.randint(8, w-9), random.randint(8, h-9)), (90, 90, 90))
    _save(s, os.path.join(OUT, 'frame.png'))

    # logo
    w, h = 460, 130
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    font = pygame.font.Font(None, 22)
    small = font.render("MYCRAFT", False, (255, 255, 255))
    big = pygame.transform.scale(small, (small.get_width()*5, small.get_height()*5))
    outline = pygame.transform.scale(font.render("MYCRAFT", False, (0, 0, 0)),
                                      (big.get_width()+12, big.get_height()+12))
    surf.blit(outline, (0, 0)); surf.blit(big, (6, 6))
    _save(surf, os.path.join(OUT, 'logo.png'))

    # icon
    w = 64
    s = pygame.Surface((w, w), pygame.SRCALPHA)
    top = w // 3
    for x in range(w):
        for y in range(top):
            s.set_at((x, y), (60, random.randint(130, 175), 40))
    for x in range(w):
        for y in range(top, w):
            c = random.randint(-15, 15)
            s.set_at((x, y), (134+c, 96+c, 67+c))
    pygame.draw.rect(s, (0, 0, 0), (0, 0, w, w), 2)
    _save(s, os.path.join(OUT, 'icon.png'))
    _save_ico(s, os.path.join(OUT, 'icon.ico'))


def _save_ico(surface, path):
    w, h = surface.get_size()
    rows = []
    for y in range(h - 1, -1, -1):
        row = bytearray()
        for x in range(w):
            r, g, b, a = surface.get_at((x, y))
            row += bytes((b, g, r, a))
        rows.append(bytes(row))
    pixel_data = b''.join(rows)
    header = struct.pack('<IiiHHIIiiII', 40, w, h*2, 1, 32, 0, w*h*4, 0, 0, 0, 0)
    mask = b'\x00' * (h * ((w + 31)//32) * 4)
    bmp = header + pixel_data + mask
    icondir = struct.pack('<HHH', 0, 1, 1)
    entry = struct.pack('<BBBBHHII', w if w < 256 else 0, h if h < 256 else 0,
                        0, 0, 1, 32, len(bmp), 22)
    with open(path, 'wb') as f:
        f.write(icondir + entry + bmp)


# ===== BLOCK TEXTURES =====
def make_block_textures():
    # grass top
    s = _noise(16, 16, (95, 159, 53), 22)
    _save(s, os.path.join(BLOCKS_OUT, 'grass_top.png'))
    # grass side
    s = _noise(16, 16, (134, 96, 67), 12)
    for x in range(16):
        for y in range(4):
            s.set_at((x, y), (60 + random.randint(-10, 10), 130 + random.randint(-20, 20), 40 + random.randint(-10, 10)))
    _save(s, os.path.join(BLOCKS_OUT, 'grass_side.png'))
    # dirt
    s = _noise(16, 16, (134, 96, 67), 14)
    for _ in range(8):
        s.set_at((random.randint(0, 15), random.randint(0, 15)), (85, 55, 35))
    _save(s, os.path.join(BLOCKS_OUT, 'dirt.png'))
    # stone
    s = _noise(16, 16, (128, 128, 128), 15)
    for _ in range(12):
        s.set_at((random.randint(0, 15), random.randint(0, 15)), (95, 95, 95))
    _save(s, os.path.join(BLOCKS_OUT, 'stone.png'))
    # log side
    s = _noise(16, 16, (110, 80, 50), 8)
    for x in range(0, 16, 3):
        for y in range(16):
            s.set_at((x, y), (80, 55, 30))
    _save(s, os.path.join(BLOCKS_OUT, 'log_side.png'))
    # log top (rings)
    s = _noise(16, 16, (160, 130, 80), 10)
    for r in range(1, 8, 2):
        pygame.draw.circle(s, (110, 80, 40), (8, 8), r, 1)
    _save(s, os.path.join(BLOCKS_OUT, 'log_top.png'))
    # leaves
    s = pygame.Surface((16, 16), pygame.SRCALPHA)
    for x in range(16):
        for y in range(16):
            if random.random() < 0.85:
                s.set_at((x, y), (40 + random.randint(0, 40), 110 + random.randint(0, 60), 40 + random.randint(0, 40), 255))
            else:
                s.set_at((x, y), (0, 0, 0, 0))
    _save(s, os.path.join(BLOCKS_OUT, 'leaves.png'))
    # water
    s = pygame.Surface((16, 16), pygame.SRCALPHA)
    for x in range(16):
        for y in range(16):
            s.set_at((x, y), (50 + random.randint(-15, 15), 110 + random.randint(-15, 15), 210 + random.randint(-15, 15), 180))
    _save(s, os.path.join(BLOCKS_OUT, 'water.png'))
    # sand
    s = _noise(16, 16, (220, 200, 130), 12)
    _save(s, os.path.join(BLOCKS_OUT, 'sand.png'))
    # planks
    s = _noise(16, 16, (180, 140, 90), 8)
    for y in range(0, 16, 4):
        for x in range(16):
            s.set_at((x, y), (130, 95, 60))
    _save(s, os.path.join(BLOCKS_OUT, 'planks.png'))
    # craft table top (planks + grid)
    s = _noise(16, 16, (160, 120, 80), 8)
    for x in range(0, 16, 4):
        for y in range(16):
            s.set_at((x, y), (90, 65, 40))
    for y in range(0, 16, 4):
        for x in range(16):
            s.set_at((x, y), (90, 65, 40))
    _save(s, os.path.join(BLOCKS_OUT, 'craft_table_top.png'))
    # craft table side (planks + tools)
    s = _noise(16, 16, (180, 140, 90), 8)
    for x in range(16):
        s.set_at((x, 5), (90, 65, 40))
    # draw small hammer
    pygame.draw.rect(s, (80, 60, 40), (4, 8, 2, 6))
    pygame.draw.rect(s, (150, 150, 150), (3, 7, 4, 2))
    pygame.draw.rect(s, (80, 60, 40), (10, 8, 2, 6))
    pygame.draw.rect(s, (150, 150, 150), (9, 7, 4, 2))
    _save(s, os.path.join(BLOCKS_OUT, 'craft_table_side.png'))


# ===== ITEM TEXTURES =====
def make_item_textures():
    def blank():
        return pygame.Surface((16, 16), pygame.SRCALPHA)

    # stick
    s = blank()
    pygame.draw.rect(s, (110, 70, 30), (7, 2, 2, 12))
    pygame.draw.rect(s, (80, 50, 20), (7, 13, 2, 1))
    _save(s, os.path.join(ITEMS_OUT, 'item_stick.png'))

    # pickaxe
    s = blank()
    pygame.draw.rect(s, (110, 70, 30), (7, 6, 2, 9))  # handle
    pygame.draw.rect(s, (180, 140, 90), (2, 3, 12, 3))  # head
    pygame.draw.rect(s, (140, 100, 60), (2, 3, 12, 1))
    pygame.draw.rect(s, (140, 100, 60), (2, 3, 1, 3))
    pygame.draw.rect(s, (140, 100, 60), (13, 3, 1, 3))
    _save(s, os.path.join(ITEMS_OUT, 'item_pickaxe.png'))

    # axe
    s = blank()
    pygame.draw.rect(s, (110, 70, 30), (7, 6, 2, 9))
    pygame.draw.polygon(s, (180, 140, 90), [(3, 2), (13, 2), (13, 7), (8, 7), (8, 4), (3, 4)])
    pygame.draw.polygon(s, (140, 100, 60), [(3, 2), (13, 2), (13, 7), (8, 7), (8, 4), (3, 4)], 1)
    _save(s, os.path.join(ITEMS_OUT, 'item_axe.png'))

    # shovel
    s = blank()
    pygame.draw.rect(s, (110, 70, 30), (7, 6, 2, 9))
    pygame.draw.polygon(s, (180, 140, 90), [(4, 2), (12, 2), (13, 6), (7, 6)])
    pygame.draw.polygon(s, (140, 100, 60), [(4, 2), (12, 2), (13, 6), (7, 6)], 1)
    _save(s, os.path.join(ITEMS_OUT, 'item_shovel.png'))

    # sword
    s = blank()
    pygame.draw.rect(s, (110, 70, 30), (7, 11, 2, 4))  # handle
    pygame.draw.rect(s, (80, 50, 20), (5, 11, 6, 1))   # guard
    pygame.draw.rect(s, (220, 220, 220), (7, 2, 2, 9))  # blade
    pygame.draw.rect(s, (170, 170, 170), (7, 2, 1, 9))
    pygame.draw.polygon(s, (220, 220, 220), [(7, 2), (9, 2), (8, 0)])
    _save(s, os.path.join(ITEMS_OUT, 'item_sword.png'))


def main():
    os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
    pygame.init()
    pygame.display.set_mode((1, 1))
    for d in (OUT, BLOCKS_OUT, ITEMS_OUT):
        os.makedirs(d, exist_ok=True)
    random.seed(42)
    make_ui_assets()
    make_block_textures()
    make_item_textures()
    print('Assets ->', OUT, BLOCKS_OUT, ITEMS_OUT)


if __name__ == '__main__':
    main()
