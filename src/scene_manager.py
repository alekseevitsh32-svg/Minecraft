class SceneManager:
    def __init__(self, scene):
        self.current = scene

    def switch(self, scene):
        self.current = scene

    def handle_event(self, e):
        self.current.handle_event(e)

    def update(self, dt):
        self.current.update(dt)

    def draw(self, surf):
        self.current.draw(surf)
