import random
import pygame
from src.scenes.base_scene import BaseScene
from src.ui.button import Button
from src.ui.text import draw_text, render_text
from src.ui.imageload import load
from src import config

SPLASHES = [
    "Всё в пикселях!",
    "100% Python!",
    "Тоже Minecraft!",
    "Не нужен Java!",
    "Кубики!!!",
    "Сделано вручную!",
    "Без ассетов!",
    "Только код!",
]


class MainMenu(BaseScene):
    def __init__(self, app):
        super().__init__(app)
        self.splash = random.choice(SPLASHES)
        self.splash_angle = 0.0
        self.splash_speed = 25.0
        self.bg = None

        cx = config.WIDTH // 2
        by = 210
        self.buttons = [
            Button(cx - 100, by, 200, 40, "Одиночная игра", self.on_play),
            Button(cx - 100, by + 55, 200, 40, "Настройки", self.on_settings),
            Button(cx - 100, by + 110, 200, 40, "Выход", self.on_exit),
        ]

    def _bg(self):
        if self.bg is None:
            tile = load('dirt.png', (48, 48))
            bg = pygame.Surface((config.WIDTH, config.HEIGHT))
            for x in range(0, config.WIDTH, 48):
                for y in range(0, config.HEIGHT, 48):
                    bg.blit(tile, (x, y))
            ov = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
            ov.fill((0, 0, 0, 130))
            bg.blit(ov, (0, 0))
            self.bg = bg
        return self.bg

    def on_play(self):
        from src.scenes.world_select import WorldSelect
        self.app.scene_manager.switch(WorldSelect(self.app))

    def on_settings(self):
        from src.scenes.settings_menu import SettingsMenu
        self.app.scene_manager.switch(SettingsMenu(self.app))

    def on_exit(self):
        self.app.running = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.app.running = False
            return
        for b in self.buttons:
            b.handle_event(event)

    def update(self, dt):
        self.splash_angle += dt * self.splash_speed
        if self.splash_angle > 18:
            self.splash_angle = 18
            self.splash_speed = -abs(self.splash_speed)
        if self.splash_angle < -18:
            self.splash_angle = -18
            self.splash_speed = abs(self.splash_speed)

    def _splash_surface(self):
        base = render_text(self.splash, 8, (255, 255, 60), 2)
        sh = render_text(self.splash, 8, (0, 0, 0), 2)
        surf = pygame.Surface((base.get_width() + 3, base.get_height() + 3),
                              pygame.SRCALPHA)
        surf.blit(sh, (2, 2))
        surf.blit(base, (0, 0))
        return surf

    def draw(self, surf):
        surf.blit(self._bg(), (0, 0))

        logo = load('logo.png')
        surf.blit(logo, (config.WIDTH // 2 - logo.get_width() // 2, 40))

        rotated = pygame.transform.rotate(self._splash_surface(), self.splash_angle)
        surf.blit(rotated, (config.WIDTH // 2 + 70, 150))

        for b in self.buttons:
            b.draw(surf)

        draw_text(surf, "v0.1 alpha", 12, config.HEIGHT - 30,
                  size=8, scale=2, color=(200, 200, 200))
        draw_text(surf, "ESC = выход", config.WIDTH - 12, config.HEIGHT - 30,
                  size=8, scale=2, color=(200, 200, 200), right=True)
