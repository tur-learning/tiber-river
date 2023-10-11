import pygame
from pygame.locals import QUIT
from shapely.geometry import LineString
from shapely.geometry import Point


def leggi_dati_da_file(filename, h):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    coords = []
    for line in lines:
        # Rimuove spazi bianchi in eccesso (come spazi e caratteri di nuova riga)
        stripped_line = line.strip()
        # Salta le righe vuote
        if not stripped_line:
            continue
        x, y = stripped_line.split(',')
        coords.append((float(x), h-float(y)))
    return coords



# Inizializza pygame
pygame.init()

# Dimensioni dello schermo
WIDTH, HEIGHT = 1600, 900

background = pygame.image.load('mappa_screenshot.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # ridimensiona lo sfondo alle dimensioni della finestra

# Crea una finestra
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Rappresentazione Punti')

# Colori
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Leggi le coordinate dal file
coords = leggi_dati_da_file('output_coordinates.txt', HEIGHT)
line = LineString(coords)
# Definisci la distanza di allargamento
buffer_distance = 30  # Sostituisci con la distanza desiderata
# Crea un buffer attorno alla LineString originale
buffered_line = line.buffer(buffer_distance)
# extract outer ring
outer_ring = buffered_line.exterior

# Define the character's starting position
character_pos = [1040, 476]
character_speed = 1

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    old_pos = Point(character_pos[0], character_pos[1])

    # Get the keyboard input for character movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        character_pos[0] -= character_speed
    if keys[pygame.K_RIGHT]:
        character_pos[0] += character_speed
    if keys[pygame.K_UP]:
        character_pos[1] -= character_speed
    if keys[pygame.K_DOWN]:
        character_pos[1] += character_speed
    if keys[pygame.K_LCTRL]:
        print(character_pos)

    # Create a LineString for the character's movement from the current position to the new position
    new_pos = Point(character_pos[0], character_pos[1])
    movement_line = LineString([old_pos, new_pos])

    # Check if the movement line intersects any of the lines in the LineString
    if line.intersects(movement_line) or outer_ring.intersects(movement_line):
        # If the character's movement line intersects any line, prevent the movement
        character_pos = [int(old_pos.x), int(old_pos.y)]

    # Disegna l'immagine di sfondo
    screen.blit(background, (0, 0))

    character_b = pygame.draw.circle(screen, BLUE, character_pos, 10)
    pygame.display.update(character_b)

    # Disegna la strada percorribile
    if len(line.coords) > 1:
        pygame.draw.lines(screen, RED, False, list(line.coords), 5)
        pygame.draw.lines(screen, RED, False, list(outer_ring.coords), 5)


    pygame.display.flip()

pygame.quit()
