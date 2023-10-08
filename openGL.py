import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import math
import overpy
from shapely import LineString
import numpy as np

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
camera_position = np.array([12.4716, 41.9149, 0.004])
line_coords = get_tiber()

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
    global x_eye, y_eye, trans_x, trans_y, rot_z
    global line_coords, camera_position, width
    # Calcolo della posizione della camera in base alla rotazione attorno all'asse Z
    x_eye = math.sin(math.radians(rot_z))
    y_eye = math.cos(math.radians(rot_z))

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Set up perspective projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fov, 16/9, 1.0, 2.0)  # 45° field of view, 1:1 aspect ratio, near and far planes

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    # Set up camera position and orientation
    #gluLookAt(x_eye, y_eye, 1,  # Eye position (camera position)
    #          x_eye, 1, -1,  # Look-at point (camera is looking at this point)
    #          0, 1, 0)  # Up vector (camera's up direction)
    
    # Utilizzo delle variabili di traslazione e rotazione per impostare la camera
    gluLookAt(x_eye + trans_x, y_eye + trans_y, 1,  # Eye position (camera position)
              0 + trans_x, 0 + trans_y, -1,  # Look-at point (camera is looking at this point)
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
            glVertex3f(55*(x-camera_position[0]), 74*(y-camera_position[1]), 0)  # Z è impostato a 0, ma puoi modificarlo come preferisci
        glEnd()  # Termina la sequenza


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
    global rot_z, trans_x, trans_y
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
    glutPostRedisplay()

def main():
    global texture_id

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutCreateWindow('Display PNG with PyOpenGL in Perspective')
    glutDisplayFunc(display)
    glEnable(GL_DEPTH_TEST)  # Enable depth testing
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)

    texture_id = load_texture("printmaps_1.png")

    glutMainLoop()

if __name__ == "__main__":
    main()
