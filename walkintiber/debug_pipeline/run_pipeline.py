from utils import views, mercator, settings, vitruvius, elevator
import os, glob

bbox = "41.88856,12.47106,41.89253,12.48202" # Isola Tiberina
#bbox = "41.7020,12.6693,41.7588,12.7265" # Albano
# bbox = "41.88864,12.47368,41.89331,12.48426"# Tiber

views.get_osm(bbox)
vitruvius.osm2obj()

# Construct the pattern
pattern = os.path.join(settings.OBJ_DIR, '*.obj')

# Get list of files matching the pattern
matching_files = glob.glob(pattern)

# Create an Elevator object
dem_file = '/home/dario/Downloads/N205E450.tif' 
EV = elevator.Elevator(dem_file, bbox)
# create the ground surface
print("Creating 3D ground object")
EV.create_3d_obj(settings.OBJ_DIR+"ground.obj", EV.lons, EV.lats, EV.dem_subset)

# Apply elevation to the other models
for file in matching_files:
    print(f"\nModifying elevation data for file {file}")
    elevator.elevate(file, EV)