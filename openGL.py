import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import math
import overpy
from shapely import LineString
import numpy as np
import osmnx as ox
import geopandas as gpd

def get_buildings():
    api = overpy.Overpass()

    result = api.query("""
        (
            way ["building"](41.8700,12.4060,41.9257,12.5193);
            relation ["building"](41.8700,12.4060,41.9257,12.5193);
        );
        (._;>;);
        out body;
    """)
    print(result)

def open_building():
    # Carica il file .osm come un GeoDataFrame
    #gdf = gpd.read_file('test_map.osm', layer='buildings')

    # Filtra solo gli edifici
    #buildings = gdf[gdf['building'].notnull()]
    buildings = [[(41.8920521, 12.4734894),
                  (41.8920683, 12.4733109),
                  (41.8918796, 12.4732428),
                  (41.8918522, 12.4734513)]]
    return buildings


def get_tiber():
    # Crea un'istanza del client Overpy
    api = overpy.Overpass()

    result = api.query("""
        (
            way(15523438);
        );
        (._;>;);
        out body;
    """)

    # Estrai le coordinate delle highway pedonali e crea oggetti LineString
    pedestrian_lines = []
    for way in result.ways:
        nodes = way.get_nodes(resolve_missing=True)
        coords = [(float(node.lon), float(node.lat)) for node in nodes]
        line = LineString(coords)
        pedestrian_lines.append(line)

    line_coords = [list(line.coords) for line in pedestrian_lines]
    return line_coords

fov = 45.0
x_eye = 0.
y_eye = 0.
trans_x = 0.
trans_y = -1.
rot_z = 180.
width = 10.
height = 1.
camera_position = np.array([12.47, 41.89, 0.004])
line_coords = get_tiber()
buildings = open_building()

def draw_cube(coords):
    vertices = [[55*(x-camera_position[0]), 74*(y-camera_position[1]), 0] for y, x in coords]
    vertices += [[55*(x-camera_position[0]), 74*(y-camera_position[1]), 0.05] for y, x in coords]
    glBegin(GL_QUADS)

    # Define the six faces of the cube
    # Bottom face
    glVertex3fv(vertices[0])
    glVertex3fv(vertices[1])
    glVertex3fv(vertices[2])
    glVertex3fv(vertices[3])

    # Top face
    glVertex3fv(vertices[4])
    glVertex3fv(vertices[5])
    glVertex3fv(vertices[6])
    glVertex3fv(vertices[7])

    # Back face
    glVertex3fv(vertices[0])
    glVertex3fv(vertices[4])
    glVertex3fv(vertices[5])
    glVertex3fv(vertices[1])
    
    # Left face
    glVertex3fv(vertices[1])
    glVertex3fv(vertices[5])
    glVertex3fv(vertices[6])
    glVertex3fv(vertices[2])

    # Front face
    glVertex3fv(vertices[2])
    glVertex3fv(vertices[6])
    glVertex3fv(vertices[7])
    glVertex3fv(vertices[3])

    # Right face
    glVertex3fv(vertices[3])
    glVertex3fv(vertices[7])
    glVertex3fv(vertices[4])
    glVertex3fv(vertices[0])

    glEnd()

def transform_and_filter_coordinates(coords, projection_matrix, modelview_matrix, viewport):
    transformed_coords = []
    for (x, y) in coords:
        screen_x, screen_y, _ = gluProject(x, y, 0, modelview_matrix, projection_matrix, viewport)
        
        # Controlla se le coordinate sono all'interno del viewport
        #if 0 <= screen_x <= viewport[2] and 0 <= screen_y <= viewport[3]:
        transformed_coords.append((screen_x, screen_y))
    return transformed_coords


def load_texture(image_path):
    img = Image.open(image_path)
    img_data = img.tobytes("raw", "RGBA", 0, -1)
    width, height = img.size

    # Generate a new texture ID and bind it
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    # Set texture parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Upload the image data to GPU memory
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    return texture_id

def display():
    global fov
    global x_eye, y_eye, trans_x, trans_y, rot_z, height
    global line_coords, camera_position, width
    global buildings
    # Calcolo della posizione della camera in base alla rotazione attorno all'asse Z
    x_eye = math.sin(math.radians(rot_z))
    y_eye = math.cos(math.radians(rot_z))

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Set up perspective projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fov, 16/9, 0.1, 10.0)  # 45° field of view, 1:1 aspect ratio, near and far planes

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    #glRotatef(rot_z-180, 0, 1, 0)
    
    # Set up camera position and orientation
    #gluLookAt(x_eye, y_eye, 1,  # Eye position (camera position)
    #          x_eye, 1, -1,  # Look-at point (camera is looking at this point)
    #          0, 1, 0)  # Up vector (camera's up direction)
    
    # Utilizzo delle variabili di traslazione e rotazione per impostare la camera
    gluLookAt(x_eye + trans_x, y_eye + trans_y, height,  # Eye position (camera position)
              0 + trans_x, 0 + trans_y, -height,  # Look-at point (camera is looking at this point)
              0, 0, 1)  # Up vector (camera's up direction along Z-axis)

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-1.0, -1.0, 0.0)
    glTexCoord2f(1, 0); glVertex3f( 1.0, -1.0, 0.0)
    glTexCoord2f(1, 1); glVertex3f( 1.0,  1.0, 0.0)
    glTexCoord2f(0, 1); glVertex3f(-1.0,  1.0, 0.0)
    glEnd()

    glLineWidth(width)
    for coords in line_coords:
        glBegin(GL_LINE_STRIP)  # Inizia a disegnare segmenti di linea
        for (x, y) in coords:
            #print(55*(x-camera_position[0]), 74*(y-camera_position[1]))
            glVertex3f(55*(x-camera_position[0]), 74*(y-camera_position[1]), 0.)  # Z è impostato a 0, ma puoi modificarlo come preferisci
        glEnd()  # Termina la sequenza

    #for building in buildings.geometry:
    #    if building.geom_type == 'Polygon':
    #        x, y = building.exterior.xy
    #        vertices = list(zip(55*(x-camera_position[0]), 74*(y-camera_position[1]), [0]*len(x)))  # Qui stiamo supponendo che l'altezza sia 0 per semplicità
    #        # ... aggiungi il codice per renderizzare il poligono con OpenGL ...

    for coords in buildings:
        draw_cube(coords)
        #glBegin(GL_QUADS)  # Inizia a disegnare segmenti di linea
        #for y, x in coords:
        #    #print(55*(x-camera_position[0]), 74*(y-camera_position[1]))
        #    glVertex3f(55*(x-camera_position[0]), 74*(y-camera_position[1]), 0.)  # Z è impostato a 0, ma puoi modificarlo come preferisci
        #    glVertex3f(55*(x-camera_position[0]), 74*(y-camera_position[1]), 0.01)
        #glEnd() 

    glDisable(GL_TEXTURE_2D)

    glutSwapBuffers()

def keyboard(key, x, y):
    global fov, width
    if key == b'+':
        fov -= 1.0
    elif key == b'-':
        fov += 1.0
    elif key == b'w':
        width += 1.0
    glutPostRedisplay()

def special_keys(key, x, y):
    global rot_z, trans_x, trans_y, height
    if key == GLUT_KEY_F2:
        rot_z += 1.0
    elif key == GLUT_KEY_F3:
        rot_z -= 1.0
    elif key == GLUT_KEY_UP:
        trans_y += 0.1
    elif key == GLUT_KEY_DOWN:
        trans_y -= 0.1
    elif key == GLUT_KEY_LEFT:
        trans_x -= 0.1
    elif key == GLUT_KEY_RIGHT:
        trans_x += 0.1
    elif key == GLUT_KEY_F4:
        height -= 0.01
    elif key == GLUT_KEY_F5:
        height += 0.01
    glutPostRedisplay()

def keyboard_callback(key, x, y):
    if key == b'\r':  # Questo è il codice per il tasto 'Enter'
        
        # 1. Ottieni le matrici di trasformazione
        projection_matrix = glGetDoublev(GL_PROJECTION_MATRIX)
        modelview_matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
        viewport = glGetIntegerv(GL_VIEWPORT)
        
        # 2. Applica le matrici alle coordinate
        transformed_lines = [transform_and_filter_coordinates(line, 
                                                   projection_matrix,
                                                   modelview_matrix,
                                                   viewport) for line in line_coords]
        
        # 3. Esporta le coordinate
        with open("output_coordinates.txt", "w") as file:
            for line in transformed_lines:
                for x, y in line:
                    file.write(f"{x},{y}\n")
                file.write("\n")  # Una riga vuota tra le linee per separarle


def main():
    global texture_id

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutCreateWindow('Display PNG with PyOpenGL in Perspective')
    glutDisplayFunc(display)
    glEnable(GL_DEPTH_TEST)  # Enable depth testing
    glutKeyboardFunc(keyboard)
    glutKeyboardFunc(keyboard_callback)
    glutSpecialFunc(special_keys)

    texture_id = load_texture("printmaps_0.png")

    glutMainLoop()

if __name__ == "__main__":
    main()
