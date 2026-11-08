import pygame
from src.scenes.base_scene import BaseScene
from src.ui.button import Button
from src.ui.text import draw_text
from src import config
from src import world_storage


class WorldSelect(BaseScene):
    def __init__(self, app):
        super().__init__(app)
        self.scroll = 0
        self.refresh()

        cx = config.WIDTH // 2
        self.new_btn = Button(cx - 260, config.HEIGHT - 75, 200, 40,
                              "Создать мир", self.on_create)
        self.back_btn = Button(cx + 60, config.HEIGHT - 75, 200, 40,
                               "Назад", self.on_back)

    def refresh(self):
        self.worlds = world_storage.list_worlds()

    def on_back(self):
        from src.scenes.main_menu import MainMenu
        self.app.scene_manager.switch(MainMenu(self.app))

    def on_create(self):
        idx, data = world_storage.new_world()
        self.enter_world(idx, data)

    def enter_world(self, index, data):
        from src.scenes.game_scene import GameScene
        self.app.scene_manager.switch(GameScene(self.app, index, data))

    def _world_rect(self, i):
        x = config.WIDTH // 2 - 260
        y = 100 + i * 55 - self.scroll
        return pygame.Rect(x, y, 520, 48)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.on_back()
            return
        self.new_btn.handle_event(event)
        self.back_btn.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, w in enumerate(self.worlds):
                r = self._world_rect(i)
                if r.collidepoint(event.pos):
                    data = world_storage.load_world(w['index'])
                    if data:
                        self.enter_world(w['index'], data)
                    return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            for i, w in enumerate(self.worlds):
                r = self._world_rect(i)
                if r.collidepoint(event.pos):
                    world_storage.delete_world(w['index'])
                    self.refresh()
                    return

        if event.type == pygame.MOUSEWHEEL:
            self.scroll = max(0, self.scroll - event.y * 40)

    def draw(self, surf):
        surf.fill((40, 40, 60))
        draw_text(surf, "Выбор мира", config.WIDTH // 2, 50,
                  size=12, scale=3, center=True)

        if not self.worlds:
            draw_text(surf, "Пока нет миров. Создай первый!",
                      config.WIDTH // 2, config.HEIGHT // 2 - 40,
                      size=9, scale=2, center=True, color=(180, 180, 180))
        else:
            clip = pygame.Rect(0, 90, config.WIDTH, config.HEIGHT - 180)
            old = surf.get_clip()
            surf.set_clip(clip)
            for i, w in enumerate(self.worlds):
                r = self._world_rect(i)
                if r.bottom < clip.top or r.top > clip.bottom:
                    continue
                pygame.draw.rect(surf, (0, 0, 0), r)
                pygame.draw.rect(surf, (110, 110, 110), r.inflate(-4, -4))
                draw_text(surf, f"Мир {w['index']}: {w['name']}",
                          r.x + 12, r.centery - 8, size=9, scale=2)
                draw_text(surf, f"seed {w['seed']}",
                          r.right - 12, r.centery - 8,
                          size=8, scale=2, color=(180, 180, 180), right=True)
            surf.set_clip(old)

        draw_text(surf, "ЛКМ — играть  |  ПКМ — удалить мир",
                  config.WIDTH // 2, config.HEIGHT - 100,
                  size=8, scale=2, center=True, color=(200, 200, 200))
        self.new_btn.draw(surf)
        self.back_btn.draw(surf)
