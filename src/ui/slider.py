import pygame
from src.ui.imageload import load


class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, value):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val, self.max_val = min_val, max_val
        self.value = value
        self.dragging = False
        self.track = load('slider_track.png', (w, h))
        self.handle = load('slider_handle.png', (12, h + 4))

    def _ratio(self):
        span = (self.max_val - self.min_val) or 1
        return (self.value - self.min_val) / span

    def _hx(self):
        return self.rect.x + int((self.rect.w - self.handle.get_width()) * self._ratio())

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            hr = pygame.Rect(self._hx() - 4, self.rect.y - 4,
                             self.handle.get_width() + 8,
                             self.handle.get_height() + 8)
            if hr.collidepoint(event.pos) or self.rect.collidepoint(event.pos):
                self.dragging = True
                self._set(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._set(event.pos[0])

    def _set(self, mx):
        rel = (mx - self.rect.x) / self.rect.w
        rel = max(0.0, min(1.0, rel))
        self.value = self.min_val + rel * (self.max_val - self.min_val)

    def draw(self, surf):
        surf.blit(self.track, self.rect)
        surf.blit(self.handle, (self._hx(), self.rect.y - 2))
