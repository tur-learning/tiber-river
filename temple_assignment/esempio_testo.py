import pygame
import sys

# Inizializza pygame
pygame.init()

# Imposta le dimensioni della finestra di gioco
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)

# Imposta un titolo per la finestra
pygame.display.set_caption("Demo di gioco")

# Scegli un font e una dimensione per il tuo testo
font = pygame.font.Font(None, 36)

# Crea il testo che vuoi mostrare. Ogni riga sarà un nuovo elemento in una lista
text_lines = [
    "Benvenuto nel gioco!",
    "Usa le FRECCE per muoverti",
    "Premi SPAZIO per saltare",
    # Aggiungi qui altre istruzioni se necessario
]

# Crea una lista di superfici di testo renderizzato
text_surfaces = [font.render(line, True, (255, 255, 255)) for line in text_lines]

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Riempi lo sfondo con un colore (nero in questo caso)
    screen.fill((0, 0, 0))

    # Posiziona le righe di testo una sopra l'altra
    y_position = 10  # La posizione y iniziale per il primo testo
    for surface in text_surfaces:
        # Blit (cioè "disegna") ogni superficie di testo una sopra l'altra, aggiornando la posizione y ogni volta
        screen.blit(surface, (10, y_position))
        y_position += surface.get_height() + 10  # Aggiusta la posizione y per la prossima riga

    # Aggiorna il display di gioco con le modifiche fatte
    pygame.display.flip()

# Termina pygame
pygame.quit()
sys.exit()
