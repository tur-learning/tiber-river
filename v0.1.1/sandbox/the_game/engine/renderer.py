import pygame

class ImageRenderer:
    def __init__(self, width, height, image_path):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pygame Blit OOP Example")
        self.image = self.load_image(image_path)

    def load_image(self, image_path):
        return pygame.image.load(image_path)

    def render(self):
        self.screen.blit(self.image, (0, 0))
        pygame.display.flip()
