import pygame
from src.scenes.base_scene import BaseScene
from src.ui.button import Button
from src.ui.slider import Slider
from src.ui.toggle import Toggle
from src.ui.dropdown import Dropdown
from src.ui.text import draw_text
from src.ui.imageload import load
from src import config

GRAPHICS = ['Быстрая', 'Обычная', 'Красивая']


class SettingsMenu(BaseScene):
    def __init__(self, app):
        super().__init__(app)
        s = app.settings
        cx = config.WIDTH // 2
        lx = cx - 100

        self.volume = Slider(lx, 125, 200, 20, 0, 100, s['volume'])
        self.fov = Slider(lx, 190, 200, 20, 30, 110, s['fov'])
        self.graphics = Dropdown(lx, 255, 200, 30, GRAPHICS, s['graphics'])
        self.fullscreen = Toggle(lx, 305, 200, 30, 'Полный экран', s['fullscreen'])
        self.done = Button(lx, 380, 200, 40, "Готово", self.on_done)

        self.widgets = [self.volume, self.fov, self.graphics,
                        self.fullscreen, self.done]

    def on_done(self):
        s = self.app.settings
        s['volume'] = int(self.volume.value)
        s['fov'] = int(self.fov.value)
        s['graphics'] = self.graphics.selected_index
        s['fullscreen'] = self.fullscreen.value
        self.app.save_settings()
        from src.scenes.main_menu import MainMenu
        self.app.scene_manager.switch(MainMenu(self.app))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.on_done()
            return
        for w in self.widgets:
            w.handle_event(event)

    def draw(self, surf):
        surf.fill((35, 35, 55))
        frame = load('frame.png')
        fx = config.WIDTH // 2 - frame.get_width() // 2
        surf.blit(frame, (fx, 30))

        cx = config.WIDTH // 2
        lx = cx - 100
        draw_text(surf, "Настройки", cx, 75, size=12, scale=3, center=True)
        draw_text(surf, f"Громкость: {int(self.volume.value)}", lx, 105,
                  size=8, scale=2)
        draw_text(surf, f"Обзор (FOV): {int(self.fov.value)}", lx, 170,
                  size=8, scale=2)
        draw_text(surf, "Графика:", lx, 235, size=8, scale=2)

        for w in self.widgets:
            w.draw(surf)
