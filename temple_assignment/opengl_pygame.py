import sys
import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
#from OpenGL.GLUT import *
from PIL import Image
import asyncio

class OBJLoader:
    def __init__(self, filename):
        self.vertices = []
        self.faces = []
        
        try:
            with open(filename, 'r') as f:
                for line in f:
                    if line[:2] == "v ":  # vertices
                        index1 = line.find(" ") + 1
                        index2 = line.find(" ", index1 + 1)
                        index3 = line.find(" ", index2 + 1)

                        vertex = (float(line[index1:index2]), float(line[index2:index3]), float(line[index3:-1]))
                        vertex = (round(vertex[0], 2), round(vertex[1], 2), round(vertex[2], 2))
                        self.vertices.append(vertex)

                    elif line[0] == "f":  # faces
                        string = line.replace("//", "/")
                        
                        i = string.find(" ") + 1
                        face = []
                        for item in range(string.count(" ")):
                            if string.find(" ", i) == -1:
                                face.append(string[i:-1])
                                break
                            face.append(string[i:string.find(" ", i)])
                            i = string.find(" ", i) + 1
                        self.faces.append(tuple(face))
                        
        except IOError:
            print(".obj file not found.")

    def render_scene(self):
        if not self.vertices:
            return

        glBegin(GL_TRIANGLES)
        for face in self.faces:
            for f in face:
                f = f.split('/')
                glVertex3fv(self.vertices[int(f[0]) - 1])
        glEnd()

class Character:
    def __init__(self):
        self.position = [0, 0, 0]  # la posizione iniziale del personaggio

    def draw(self):
        """ Disegna il personaggio. Qui useremo un semplice cubo senza GLUT. """
        d = 0.004
        vertices = [  # Vertici per un cubo
            [-d, -d, -d], [d, -d, -d], [d, d, -d], [-d, d, -d],
            [-d, -d, d], [d, -d, d], [d, d, d], [-d, d, d]
        ]

        edges = [  # Spigoli che definiscono ogni faccia del cubo
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]

        faces = [  # Vertici per ogni faccia del cubo
            (0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4),
            (2, 3, 7, 6), (0, 3, 7, 4), (1, 2, 6, 5)
        ]

        glPushMatrix()  # Salva la matrice corrente
        glTranslate(self.position[0], self.position[1], self.position[2])  # Trasla il cubo

        # Disegna le facce del cubo
        glBegin(GL_QUADS)
        for face in faces:
            for vertex in face:
                glVertex3fv(vertices[vertex])  # Aggiunge i vertici della faccia
        glEnd()

        # Disegna gli spigoli del cubo (opzionale, per un aspetto più definito)
        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()

        glPopMatrix()  # Ripristina la matrice precedente

    # def __init__(self, obj_file, position=(0, 0, 0)):
    #     self.obj = OBJLoader(obj_file)
    #     self.position = position

    # def draw(self):
    #     glPushMatrix()
    #     glTranslate(self.position[0], self.position[1], self.position[2])
    #     self.obj.render_scene()
    #     glPopMatrix()

    def move(self, direction):
        """ Aggiorna la posizione del personaggio in base al comando dell'utente. """
        l = 0.001
        if direction == 'FORWARD':
            self.position[1] += l
        elif direction == 'BACKWARD':
            self.position[1] -= l
        elif direction == 'LEFT':
            self.position[0] -= l
        elif direction == 'RIGHT':
            self.position[0] += l


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
        self.load_texture("printmaps.png")
        #self.character = Character('character.obj', position=(0, 0, 0))
        self.character = Character()

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
        # Controlla i tasti per muovere il personaggio
        if keys[pygame.K_w]:
            self.character.move('FORWARD')
        if keys[pygame.K_s]:
            self.character.move('BACKWARD')
        if keys[pygame.K_a]:
            self.character.move('LEFT')
        if keys[pygame.K_d]:
            self.character.move('RIGHT')
        """ if keys[pygame.K_w]:
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
            self.update_origin() """
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
        self.character.draw()

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