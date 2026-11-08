import pygame
from src import config

_cache = {}


def load(name, size=None):
    key = (name, size)
    if key in _cache:
        return _cache[key]
    img = pygame.image.load(config.asset(name)).convert_alpha()
    if size:
        img = pygame.transform.scale(img, size)
    _cache[key] = img
    return img
