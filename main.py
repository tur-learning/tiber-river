import pygame
from shapely.geometry import LineString
from shapely.geometry import Point
from shapely import transform
from shapely.affinity import translate, scale
from shapely.ops import linemerge, unary_union
from shapely.wkt import loads
import overpy
from ast import literal_eval

bbox_lat = 41.89100; bbox_lon = 12.47750
bbox_dx = 0.002; bbox_dy = 0.001
zoom = 1
bbox_dx, bbox_dy = zoom*bbox_dx, zoom*bbox_dy

def get_streets():
    api = overpy.Overpass()

    # lungotevere = 41.8700,12.4060,41.9257,12.5193
    bbox = f"{bbox_lat - bbox_dy}, {bbox_lon - bbox_dx}, {bbox_lat + bbox_dy},  {bbox_lon + bbox_dx}"
    print(bbox)

    qbox = literal_eval(bbox)

    # way(%s) ["highway"~"^(pedestrian|footway|residential|living_street|steps|cycleway|path|service|secondary|tertiary)$"];
    # way(%s) ["barrier"~"^(kerb|retaining_wall)$"];
    # relation(%s) ["highway"~"^(pedestrian|footway|residential|living_street|steps|pedestrian|cycleway|path|service)$"];

    query = """
        (
        relation(%s) ["type"="multipolygon"]["highway"="pedestrian"];
        way(%s) ["highway"~"^(pedestrian|footway|residential|living_street|steps|cycleway|path|service|secondary|tertiary)$"];
        way(%s) ["barrier"~"^(kerb|retaining_wall)$"];
        relation(%s) ["highway"~"^(pedestrian|footway|residential|living_street|steps|pedestrian|cycleway|path|service)$"];
        );
        (._;>;);
        out body;
        """ % (bbox, bbox, bbox, bbox)
    response = api.query(query)

    lss = [] #convert ways to linstrings

    for ii_w,way in enumerate(response.ways):
        try: 
            # if ("Lungotevere" in way.tags.get("name")): 
                ls_coords = []

                for n,node in enumerate(way.nodes):
                    ls_coords.append((node.lon,node.lat)) # create a list of node coordinates

                lss.append(LineString(ls_coords)) # create a LineString from coords

        except:
            continue

    merged = linemerge([*lss]) # merge LineStrings
    borders = unary_union(merged) # linestrings to a MultiLineString

    multilinestring = str(borders)
    multiline = loads(multilinestring)
    return multiline


#coordinates = "LINESTRING (12.4750809 41.8899964, 12.4752331 41.8899546, 12.4751878 41.8898632, 12.4750356 41.8899049, 12.4750241 41.8899244, 12.4750276 41.8899649, 12.4750809 41.8899964)"
#coordinates = "MULTILINESTRING ((12.4750809 41.8899964, 12.4752331 41.8899546, 12.4751878 41.8898632, 12.4750356 41.8899049, 12.4750241 41.8899244, 12.4750276 41.8899649, 12.4750809 41.8899964), (12.4753672 41.8899177, 12.475546 41.8898687, 12.4755098 41.8897956, 12.4753311 41.8898447, 12.4753672 41.8899177), (12.4756299 41.8897038, 12.4748784 41.8898938, 12.4748532 41.8899171, 12.4748729 41.8901466, 12.4749174 41.8901726, 12.4757531 41.8899472, 12.4756299 41.8897038))"
coordinates = get_streets()
# coordinates = transform(coordinates, lambda x: (x - [12.473,41.889]))
# coordinates = transform(coordinates, lambda x: (x * [100000, 100000]))

# Now the LineStrings are scaled and centered within the screen dimensions of (1000, 1000)

# Initialize pygame
pygame.init()
width, height = 1600, 800
screen = pygame.display.set_mode((width, height))

# Clear the screen
screen.fill((0, 0, 0))

# Calculate the center coordinates of the LineStrings
center_x = bbox_lon
center_y = bbox_lat

# Calculate the scaling factors to fit the LineStrings within the screen dimensions
zoom_factor = 1
scale_x = width / (bbox_dx/zoom_factor)#; print(scale_x)
scale_y = height / (bbox_dy/zoom_factor)#; print(scale_y)

# Apply transformations to fit and center the LineStrings within the screen
coordinates = translate(coordinates, -center_x, -center_y)
coordinates = scale(coordinates, min(scale_x, scale_y), min(scale_x, scale_y))
coordinates = translate(coordinates, width/2, height/2)  # Center the LineStrings within the screen

# Flip the lines only
# flipped_coordinates = coordinates.clone()  # Create a copy of the coordinates
flipped_lines = []
for line in coordinates.geoms:
    flipped_line = LineString([(x, height - y) for x, y in line.coords])
    pygame.draw.lines(screen, (0, 255, 0), False, flipped_line.coords[:], 2)
    flipped_lines.append(flipped_line)

merged = linemerge([*flipped_lines]) # merge LineStrings
borders = unary_union(merged) # linestrings to a MultiLineString

multilinestring = str(borders)
coordinates = loads(multilinestring)

screen.fill((0, 0, 0))

for line in coordinates.geoms:
    pygame.draw.lines(screen, (0, 255, 0), False, line.coords[:], 2)

# Update the display
pygame.display.flip()

# Define the character's starting position
character_pos = [width // 2, height // 2]
character_speed = 1

player = pygame.image.load('dis.png').convert_alpha()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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

    # Create a LineString for the character's movement from the current position to the new position
    new_pos = Point(character_pos[0], character_pos[1])
    movement_line = LineString([old_pos, new_pos])

    # Check if the movement line intersects any of the lines in the LineString
    if coordinates.intersects(movement_line):
        # If the character's movement line intersects any line, prevent the movement
        character_pos = [int(old_pos.x), int(old_pos.y)]

    # Draw the character
    character_a = pygame.draw.circle(screen, (0, 0, 0), (int(old_pos.x), int(old_pos.y)), 10)
    character_b = pygame.draw.circle(screen, (255, 0, 0), character_pos, 10)
    # screen.blit(player, character_pos)

    # Clear the screen
    # character.fill((0, 0, 0))

    # # Draw the area outlined by the LineString
    for line in coordinates.geoms:
        pygame.draw.lines(screen, (0, 255, 0), False, line.coords[:], 2)

    # # Flip the lines only
    # # flipped_coordinates = coordinates.clone()  # Create a copy of the coordinates
    # for line in coordinates.geoms:
    #     flipped_line = LineString([(x, height - y) for x, y in line.coords])
    #     pygame.draw.lines(screen, (0, 255, 0), False, flipped_line.coords[:], 2)

    # # Flip the entire screen vertically
    # flipped_screen = pygame.transform.flip(screen, False, True)

    # # Update the flipped screen
    # screen.blit(flipped_screen, (0, 0))

    # Update the display
    # pygame.display.update(screen.get_rect())
    pygame.display.update(character_a)
    pygame.display.update(character_b)
    # pygame.display.flip()

# Quit pygame
pygame.quit()