import pygame
from src.ui.text import draw_text


class Dropdown:
    def __init__(self, x, y, w, h, options, index=0):
        self.rect = pygame.Rect(x, y, w, h)
        self.options = options
        self.selected_index = index

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.selected_index = (self.selected_index + 1) % len(self.options)
                return True
        return False

    def draw(self, surf):
        pygame.draw.rect(surf, (0, 0, 0), self.rect)
        pygame.draw.rect(surf, (110, 110, 110), self.rect.inflate(-2, -2))
        draw_text(surf, self.options[self.selected_index], *self.rect.center,
                  size=9, scale=2, center=True)
        draw_text(surf, ">", self.rect.right - 22, self.rect.centery,
                  size=9, scale=2, center=True)
