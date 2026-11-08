import pygame
from src.ui.text import draw_text
from src.ui.imageload import load


class Button:
    def __init__(self, x, y, w, h, text, on_click=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.on_click = on_click
        self.hover = False
        self.enabled = True

    def handle_event(self, event):
        if not self.enabled:
            return False
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.on_click:
                    self.on_click()
                return True
        return False

    def draw(self, surf):
        name = ('button_disabled.png' if not self.enabled
                else 'button_hover.png' if self.hover
                else 'button.png')
        surf.blit(load(name, self.rect.size), self.rect)
        color = (255, 255, 255) if self.enabled else (150, 150, 150)
        draw_text(surf, self.text, *self.rect.center,
                  size=9, color=color, scale=2, center=True)
