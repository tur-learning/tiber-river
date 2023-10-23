import pygame

class GameLoopManager:
    def __init__(self, renderer):
        self.renderer = renderer
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def main_loop(self):
        while self.running:
            self.handle_events()
            self.renderer.render()
        pygame.quit()