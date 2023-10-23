import sys
import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import asyncio

class InteractiveView:
    def __init__(self):
        self.h_angle = math.radians(30)
        self.v_angle = math.radians(45)
        self.K = 0.3
        self.X0 = 0.
        self.lx = 0.
        self.Y0 = 0.
        self.ly = 0.
        self.texture_id = None
        self.init_gl()
        self.load_texture("printmaps.png")  # Sostituisci con il tuo percorso dell'immagine

    def init_gl(self):
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (1600/900), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

    def load_texture(self, image_path):
        img = Image.open(image_path)
        img_data = img.tobytes("raw", "RGBA", 0, -1)
        width, height = img.size

        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.h_angle += math.radians(1)
        if keys[pygame.K_RIGHT]:
            self.h_angle -= math.radians(1)
        if keys[pygame.K_UP]:
            if self.v_angle < math.radians(89):
                self.v_angle += math.radians(1)
        if keys[pygame.K_DOWN]:
            if self.v_angle > math.radians(3):
                self.v_angle -= math.radians(1)
        if keys[pygame.K_w]:
            self.ly += 0.01
            self.update_origin()
        if keys[pygame.K_s]:
            self.ly -= 0.01
            self.update_origin()
        if keys[pygame.K_d]:
            self.lx += 0.01
            self.update_origin()
        if keys[pygame.K_a]:
            self.lx -= 0.01
            self.update_origin()
        if keys[pygame.K_z]:
            self.K += 0.01
        if keys[pygame.K_LCTRL]:
            print(self.lx)
            print(self.ly)
            self.update_origin()
        if keys[pygame.K_x]:
            self.K -= 0.01
        if keys[pygame.K_RETURN]:
            self.capture_screenshot()

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        gluLookAt(-self.K * math.sin(self.h_angle) * math.cos(self.v_angle) 
                            + self.X0, 
                  -self.K * math.cos(self.h_angle) * math.cos(self.v_angle) 
                            + self.Y0, 
                  self.K * math.sin(self.v_angle),
                  self.X0, self.Y0, 0,  # Look-at point
                  0, 0, 1)  # Up vector

        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex3f(-1.0, -1.0, 0.0)
        glTexCoord2f(1, 0); glVertex3f(1.0, -1.0, 0.0)
        glTexCoord2f(1, 1); glVertex3f(1.0, 1.0, 0.0)
        glTexCoord2f(0, 1); glVertex3f(-1.0, 1.0, 0.0)
        glEnd()

    def capture_screenshot(self, filename='screenshot.png'):
        """
        Cattura uno screenshot e lo salva su disco.
        """
        width, height = pygame.display.get_surface().get_size()
        screenshot = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGB", (width, height), screenshot)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)  # GL e PIL hanno coordinate Y opposte
        image.save(filename)
        print(f"Screenshot salvato come {filename}")

    def update_origin(self):
        self.X0 = self.lx * math.cos(self.h_angle) + self.ly * math.sin(self.h_angle)
        self.Y0 = - self.lx * math.sin(self.h_angle) + self.ly * math.cos(self.h_angle)


async def main():
    pygame.init()
    display = (1600, 900)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    interactive_view = InteractiveView()

    clock = pygame.time.Clock()
    running = True
    screenshot_taken = False  # Indicatore se uno screenshot è stato già catturato durante l'evento di pressione

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Rilevamento del rilascio del tasto
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    screenshot_taken = False

        interactive_view.handle_keys()

        # Verifica se il tasto è stato premuto e se uno screenshot non è stato ancora catturato
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN] and not screenshot_taken:
            interactive_view.capture_screenshot()
            screenshot_taken = True

        interactive_view.render()
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    asyncio.run(main())