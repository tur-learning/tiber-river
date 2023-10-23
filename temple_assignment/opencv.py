import cv2
import numpy as np

def main():
    # Carica l'immagine.
    image = cv2.imread('printmaps.png')

    # Controlla se l'immagine è stata caricata correttamente
    if image is None:
        print("Errore nel caricamento dell'immagine")
        return

    rows, cols = image.shape[:2]

    # Punti nell'immagine originale.
    pts_original = np.float32([[0, 0], [cols - 1, 0], [0, rows - 1], [cols - 1, rows - 1]])

    # Punti nell'immagine di destinazione. Modifica questi punti in base alle tue esigenze.
    pts_destination = np.float32([[100, 100], [cols - 1, 0], [100, rows - 1], [cols - 100, rows - 200]])
    print(pts_destination)

    # Calcola la matrice di trasformazione prospettica.
    matrix = cv2.getPerspectiveTransform(pts_original, pts_destination)
    print(matrix)

    # Applica la trasformazione prospettica all'immagine.
    result = cv2.warpPerspective(image, matrix, (cols, rows))

    # Salva l'immagine risultante.
    cv2.imwrite('mappa_trasformata.png', result)

    print("L'immagine trasformata è stata salvata con successo.")

if __name__ == "__main__":
    main()
