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
        # Initialize view angles, movement speed, and texture settings
        self.h_angle = math.radians(30)  # Horizontal viewing angle
        self.v_angle = math.radians(45)  # Vertical viewing angle
        self.K = 0.3  # Camera distance factor
        self.X0, self.Y0 = 0., 0.  # Initial origin coordinates
        self.lx, self.ly = 0., 0.  # Direction for lateral movements
        self.texture_id = None  # OpenGL texture ID
        self.screenshot_count = 0  # Counter for screenshot names
        self.return_pressed = False
        
        # Set up OpenGL and load the texture
        self.init_gl()
        self.load_texture("printmaps.png")

    def init_gl(self):
        # OpenGL initialization
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glShadeModel(GL_SMOOTH)
        # Set up perspective projection matrix
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (1600/900), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

    def load_texture(self, image_path):
        # Load an image and bind it as a 2D texture
        img = Image.open(image_path)
        img_data = img.tobytes("raw", "RGBA", 0, -1)
        width, height = img.size

        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        # Set texture parameters for scaling
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        # Upload texture data
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    def handle_keys(self):
        # Process keyboard inputs for movements and actions
        keys = pygame.key.get_pressed()
        # Adjust view angles with arrow keys
        if keys[pygame.K_LEFT]:
            self.h_angle -= math.radians(1)
        if keys[pygame.K_RIGHT]:
            self.h_angle += math.radians(1)
        # Prevent flipping over the vertical limits
        if keys[pygame.K_UP] and self.v_angle < math.radians(89):
            self.v_angle += math.radians(1)
        if keys[pygame.K_DOWN] and self.v_angle > math.radians(3):
            self.v_angle -= math.radians(1)
        # Handle W/A/S/D for movement and adjust origin
        if keys[pygame.K_w]:
            self.ly = 0.01; self.lx = 0.0; self.update_origin()
        if keys[pygame.K_s]:
            self.ly = -0.01; self.lx = 0.0; self.update_origin()
        if keys[pygame.K_d]:
            self.lx = 0.01; self.ly = 0.0; self.update_origin()
        if keys[pygame.K_a]:
            self.lx = -0.01; self.ly = 0.; self.update_origin()
        # Zoom control
        if keys[pygame.K_z]:
            self.K += 0.01
        if keys[pygame.K_x] and self.K > 0.2:
            self.K -= 0.01
        # Capture screenshot with Enter key
        if keys[pygame.K_RETURN]:
            if not self.enter_pressed:
                self.capture_screenshot()
                # Set the flag to True after taking a screenshot
                self.enter_pressed = True
        else:
            # Reset the flag if "Enter" is not pressed
            self.enter_pressed = False


    def render(self):
        # Render the scene
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Calculate camera position and set viewing direction
        gluLookAt(
            -self.K * math.sin(self.h_angle) * math.cos(self.v_angle) + self.X0,
            -self.K * math.cos(self.h_angle) * math.cos(self.v_angle) + self.Y0,
            self.K * math.sin(self.v_angle), # Camera position
            self.X0, self.Y0, 0,  # Point to look at
            0, 0, 1  # Up vector
        )

        # Draw textured quad
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex3f(-1.0, -1.0, 0.0)
        glTexCoord2f(1, 0); glVertex3f(1.0, -1.0, 0.0)
        glTexCoord2f(1, 1); glVertex3f(1.0, 1.0, 0.0)
        glTexCoord2f(0, 1); glVertex3f(-1.0, 1.0, 0.0)
        glEnd()

    def capture_screenshot(self):
        # Modify the filename to include the screenshot count
        filename = f'screenshot_{self.screenshot_count}.png'
        width, height = pygame.display.get_surface().get_size()
        screenshot = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGB", (width, height), screenshot)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)  # Correcting the y-coordinate flip
        image.save(filename)
        print(f"Screenshot saved as {filename}")
        self.screenshot_count += 1  # Increment the counter for the next screenshot


    def update_origin(self):
        # Update the origin based on the current movement direction
        self.X0 += self.lx * math.cos(self.h_angle) + self.ly * math.sin(self.h_angle)
        self.Y0 += -self.lx * math.sin(self.h_angle) + self.ly * math.cos(self.h_angle)

async def main():
    # Initialize pygame and set up the display
    pygame.init()
    display = (1600, 900)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    interactive_view = InteractiveView()

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        interactive_view.handle_keys()

        interactive_view.render()  # Draw the scene

        pygame.display.flip()
        clock.tick(60)  # Maintain 60 frames per second
        await asyncio.sleep(0)  # Yield execution back to the event loop

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    asyncio.run(main())  # Start the program
