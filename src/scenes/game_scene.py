import pygame
from src.scenes.base_scene import BaseScene
from src.ui.text import draw_text
from src.ui.imageload import load
from src import config
from src import world_storage


class GameScene(BaseScene):
    def __init__(self, app, world_index, world_data):
        super().__init__(app)
        self.world_index = world_index
        self.world_data = world_data

    def _save(self):
        world_storage.save_world(self.world_index, self.world_data)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._save()
            from src.scenes.world_select import WorldSelect
            self.app.scene_manager.switch(WorldSelect(self.app))

    def draw(self, surf):
        surf.fill((110, 160, 210))
        tile = load('grass_top.png', (32, 32))
        for x in range(0, config.WIDTH, 32):
            for y in range(config.HEIGHT - 96, config.HEIGHT, 32):
                surf.blit(tile, (x, y))

        draw_text(surf, "Тут будет игра", config.WIDTH // 2, config.HEIGHT // 2 - 20,
                  size=14, scale=3, center=True)
        draw_text(surf, f"Мир #{self.world_index} — {self.world_data.get('name', '')}",
                  config.WIDTH // 2, config.HEIGHT // 2 + 40,
                  size=9, scale=2, center=True, color=(230, 230, 230))
        draw_text(surf, f"seed: {self.world_data.get('seed', 0)}",
                  config.WIDTH // 2, config.HEIGHT // 2 + 70,
                  size=8, scale=2, center=True, color=(200, 200, 200))
        draw_text(surf, "ESC — сохранить и выйти в меню",
                  config.WIDTH // 2, config.HEIGHT - 140,
                  size=9, scale=2, center=True, color=(255, 255, 255))
