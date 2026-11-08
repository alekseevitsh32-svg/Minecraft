import pygame

_cache = {}


def render_text(text, size=8, color=(255, 255, 255), scale=3):
    key = (text, size, color, scale)
    if key in _cache:
        return _cache[key]
    font = pygame.font.Font(None, size)
    surf = font.render(text, False, color)
    if surf.get_width() == 0 or surf.get_height() == 0:
        surf = pygame.Surface((1, 1), pygame.SRCALPHA)
    surf = pygame.transform.scale(
        surf, (surf.get_width() * scale, surf.get_height() * scale))
    _cache[key] = surf
    return surf


def draw_text(surface, text, x, y, size=8, color=(255, 255, 255),
              scale=3, center=False, shadow=True, right=False):
    txt = render_text(text, size, color, scale)
    rect = txt.get_rect()
    if center:
        rect.center = (x, y)
    elif right:
        rect.topright = (x, y)
    else:
        rect.topleft = (x, y)
    if shadow:
        sh = render_text(text, size, (20, 20, 20), scale)
        if center:
            sh_rect = sh.get_rect(center=(x + scale, y + scale))
        elif right:
            sh_rect = sh.get_rect(topright=(x + scale, y + scale))
        else:
            sh_rect = sh.get_rect(topleft=(x + scale, y + scale))
        surface.blit(sh, sh_rect)
    surface.blit(txt, rect)
    return rect
