import pygame
from src.ui.text import draw_text


class Toggle:
    def __init__(self, x, y, w, h, label, value):
        self.rect = pygame.Rect(x, y, w, h)
        self.label = label
        self.value = value

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.value = not self.value

    def draw(self, surf):
        color = (100, 170, 100) if self.value else (170, 90, 90)
        pygame.draw.rect(surf, (0, 0, 0), self.rect)
        pygame.draw.rect(surf, color, self.rect.inflate(-2, -2))
        text = f"{self.label}: {'ВКЛ' if self.value else 'ВЫКЛ'}"
        draw_text(surf, text, *self.rect.center, size=9, scale=2, center=True)
