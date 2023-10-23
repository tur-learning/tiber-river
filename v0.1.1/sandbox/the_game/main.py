from engine.game_loop import GameLoopManager
from engine.renderer import ImageRenderer

def main():
    image_renderer = ImageRenderer(800, 600, 'assets/printmap.png')
    game_manager = GameLoopManager(image_renderer)
    game_manager.main_loop()

if __name__ == '__main__':
    main()