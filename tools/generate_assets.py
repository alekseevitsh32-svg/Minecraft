import os
import random
import struct
import pygame

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'textures', 'menu')


def _noise(w, h, base, var):
    s = pygame.Surface((w, h))
    for x in range(w):
        for y in range(h):
            r = max(0, min(255, base[0] + random.randint(-var, var)))
            g = max(0, min(255, base[1] + random.randint(-var, var)))
            b = max(0, min(255, base[2] + random.randint(-var, var)))
            s.set_at((x, y), (r, g, b))
    return s


def make_dirt():
    s = _noise(16, 16, (134, 96, 67), 12)
    for _ in range(10):
        s.set_at((random.randint(0, 15), random.randint(0, 15)), (85, 55, 35))
    pygame.image.save(s, os.path.join(OUT, 'dirt.png'))


def make_stone():
    s = _noise(16, 16, (128, 128, 128), 15)
    pygame.image.save(s, os.path.join(OUT, 'stone.png'))


def make_grass_top():
    s = _noise(16, 16, (95, 159, 53), 22)
    pygame.image.save(s, os.path.join(OUT, 'grass_top.png'))


def make_button(name, base, disabled=False):
    w, h = 200, 40
    s = pygame.Surface((w, h))
    s.fill(base)
    if not disabled:
        hl = tuple(min(255, c + 55) for c in base)
        sh = tuple(max(0, c - 55) for c in base)
        pygame.draw.line(s, hl, (0, 0), (w - 1, 0))
        pygame.draw.line(s, hl, (0, 0), (0, h - 1))
        pygame.draw.line(s, sh, (0, h - 1), (w - 1, h - 1))
        pygame.draw.line(s, sh, (w - 1, 0), (w - 1, h - 1))
    pygame.draw.rect(s, (0, 0, 0), (0, 0, w, h), 1)
    pygame.image.save(s, os.path.join(OUT, name))


def make_slider():
    w, h = 200, 20
    s = pygame.Surface((w, h))
    s.fill((35, 35, 35))
    pygame.draw.rect(s, (0, 0, 0), (0, 0, w, h), 1)
    pygame.draw.line(s, (65, 65, 65), (1, 1), (w - 2, 1))
    pygame.image.save(s, os.path.join(OUT, 'slider_track.png'))

    hw, hh = 12, 24
    hs = pygame.Surface((hw, hh))
    hs.fill((180, 180, 180))
    pygame.draw.line(hs, (220, 220, 220), (1, 1), (hw - 2, 1))
    pygame.draw.rect(hs, (0, 0, 0), (0, 0, hw, hh), 1)
    pygame.image.save(hs, os.path.join(OUT, 'slider_handle.png'))


def make_frame():
    w, h = 500, 420
    s = pygame.Surface((w, h))
    s.fill((198, 198, 198))
    pygame.draw.rect(s, (0, 0, 0), (0, 0, w, h), 2)
    pygame.draw.rect(s, (85, 85, 85), (2, 2, w - 4, h - 4), 2)
    pygame.draw.rect(s, (255, 255, 255), (4, 4, w - 8, h - 8), 1)
    pygame.draw.rect(s, (110, 110, 110), (5, 5, w - 10, h - 10))
    for _ in range(120):
        x = random.randint(8, w - 9)
        y = random.randint(8, h - 9)
        s.set_at((x, y), (90, 90, 90))
    pygame.image.save(s, os.path.join(OUT, 'frame.png'))


def make_logo():
    w, h = 460, 130
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    font = pygame.font.Font(None, 22)
    small = font.render("MYCRAFT", False, (255, 255, 255))
    big = pygame.transform.scale(small, (small.get_width() * 5, small.get_height() * 5))
    outline = pygame.transform.scale(
        font.render("MYCRAFT", False, (0, 0, 0)),
        (big.get_width() + 12, big.get_height() + 12)
    )
    surf.blit(outline, (0, 0))
    surf.blit(big, (6, 6))
    pygame.image.save(surf, os.path.join(OUT, 'logo.png'))


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
    header = struct.pack('<IiiHHIIiiII',
                         40, w, h * 2, 1, 32, 0, w * h * 4, 0, 0, 0, 0)
    mask = b'\x00' * (h * ((w + 31) // 32) * 4)
    bmp = header + pixel_data + mask
    icondir = struct.pack('<HHH', 0, 1, 1)
    entry = struct.pack('<BBBBHHII',
                        w if w < 256 else 0, h if h < 256 else 0,
                        0, 0, 1, 32, len(bmp), 22)
    with open(path, 'wb') as f:
        f.write(icondir + entry + bmp)


def make_icon():
    w = 64
    s = pygame.Surface((w, w), pygame.SRCALPHA)
    top = w // 3
    for x in range(w):
        for y in range(top):
            s.set_at((x, y), (60, random.randint(130, 175), 40))
    for x in range(w):
        for y in range(top, w):
            c = random.randint(-15, 15)
            s.set_at((x, y), (134 + c, 96 + c, 67 + c))
    pygame.draw.rect(s, (0, 0, 0), (0, 0, w, w), 2)
    pygame.image.save(s, os.path.join(OUT, 'icon.png'))
    _save_ico(s, os.path.join(OUT, 'icon.ico'))


def main():
    os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
    pygame.init()
    pygame.display.set_mode((1, 1))
    os.makedirs(OUT, exist_ok=True)
    random.seed(42)
    make_dirt()
    make_stone()
    make_grass_top()
    make_button('button.png', (110, 110, 110))
    make_button('button_hover.png', (130, 140, 200))
    make_button('button_disabled.png', (70, 70, 70), disabled=True)
    make_slider()
    make_frame()
    make_logo()
    make_icon()
    print('Assets ->', OUT)


if __name__ == '__main__':
    main()
