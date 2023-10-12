import pygame

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Create a screen and set the caption
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Blit Example")

# Load the image
image = pygame.image.load('printmap.png')

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the image
    screen.blit(image, (0, 0))

    # Update the display
    pygame.display.flip()

pygame.quit()
