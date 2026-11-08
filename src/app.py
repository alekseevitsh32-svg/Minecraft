import pygame
from src import config
from src.scene_manager import SceneManager
from src.settings_store import load_settings, save_settings


class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        pygame.display.set_caption("MyCraft v0.1")
        self.clock = pygame.time.Clock()
        self.running = True
        self.settings = load_settings()

        from src.scenes.main_menu import MainMenu
        self.scene_manager = SceneManager(MainMenu(self))

    def save_settings(self):
        save_settings(self.settings)

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.scene_manager.handle_event(event)
            self.scene_manager.update(dt)
            self.scene_manager.draw(self.screen)
            pygame.display.flip()
        pygame.quit()
