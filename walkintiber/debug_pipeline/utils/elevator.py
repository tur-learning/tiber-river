import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal, osr
from matplotlib.colors import LogNorm
import utils.mercator as mercator

class Elevator():
    def __init__(self, dem_file, bbox="41.88856,12.47106,41.89253,12.48202"):
        # Load the TIFF file
        # https://tinitaly.pi.ingv.it/data_1.1/w46075_s10/w46075_s10.zip
        #dem_file = '/home/dario/Downloads/w46075_s10.tif'
        self.dataset = gdal.Open(dem_file)
        band = self.dataset.GetRasterBand(1)

        coords = [float(coord) for coord in bbox.split(',')]
        self.minlat = coords[0] - 0.01
        self.minlon = coords[1] - 0.01
        self.maxlat = coords[2] + 0.01
        self.maxlon = coords[3] + 0.01

        self.av_lon_lat = [0.5*(self.minlon+self.maxlon), 
                           0.5*(self.minlat+self.maxlat)]
        # (y coordinates increase for decreasing latitude)
        x_min, y_max = self.latlon_to_pixel(self.minlon, self.minlat, self.dataset)
        x_max, y_min = self.latlon_to_pixel(self.maxlon, self.maxlat, self.dataset)

        x_min, y_min, x_max, y_max = int(x_min), int(y_min), int(x_max), int(y_max)

        self.bounds = [[x_min, y_min], [x_max, y_max]]

        # Read only the subset of the DEM data
        print(self.bounds)
        self.dem_subset = band.ReadAsArray(x_min, y_min, x_max-x_min, y_max-y_min)

        # Adjust the GeoTransform for the subset
        geo_transform = list(self.dataset.GetGeoTransform())
        geo_transform[0] += x_min * geo_transform[1]  # Adjust top-left X
        geo_transform[3] += y_min * geo_transform[5]  # Adjust top-left Y
        print(geo_transform)

        # Setup the coordinate transformation
        source_srs = osr.SpatialReference()
        source_srs.ImportFromWkt(self.dataset.GetProjection())
        target_srs = osr.SpatialReference()
        target_srs.ImportFromEPSG(4326)
        transform = osr.CoordinateTransformation(source_srs, target_srs)

        # Create arrays for latitude, longitude, and elevation
        rows, cols = self.dem_subset.shape
        print(rows, cols)
        self.lats = np.zeros_like(self.dem_subset, dtype=float)
        self.lons = np.zeros_like(self.dem_subset, dtype=float)

        # Convert each pixel to latitude and longitude
        for row in range(rows):
            for col in range(cols):
                lon, lat = self.pixel_to_latlon(col, row, geo_transform, transform)
                self.lats[row, col] = lat
                self.lons[row, col] = lon

        # Example usage:
        lon, lat = 12.461023, 41.891570  # Replace with your longitude and latitude
        #elevation = bilinear_interpolate(lon, lat, bounds, dataset, dem_subset, geo_transform)
        self.transformM = mercator.Mercator(self.av_lon_lat)

    def latlon_to_pixel(self, lon, lat, dataset):
        # Create source and target spatial references
        source_srs = osr.SpatialReference()
        source_srs.ImportFromEPSG(4326)  # WGS84

        target_srs = osr.SpatialReference()
        target_srs.ImportFromWkt(dataset.GetProjection())
        #target_srs.ImportFromEPSG(32632)  # WGS 84 / UTM zone 32N

        transform = osr.CoordinateTransformation(source_srs, target_srs)

        # Transform lat/lon to UTM
        x_utm, y_utm, _ = transform.TransformPoint(lat, lon)

        # Convert from UTM to pixel coordinates
        geo_transform = dataset.GetGeoTransform()
        x_pixel = (x_utm - geo_transform[0]) / geo_transform[1]
        y_pixel = (y_utm - geo_transform[3]) / geo_transform[5]

        return x_pixel, y_pixel
    
    def create_3d_obj(self, filename, lon, lat, elevation):
        """
        Create a .obj file from 2D numpy arrays of longitude, latitude, and elevation data.

        :param lon: 2D numpy array of longitudes
        :param lat: 2D numpy array of latitudes
        :param elevation: 2D numpy array of elevations
        :param filename: Name of the .obj file to be created
        """
        def calculate_normal(v1, v2, v3):
            """
            Calculate the normal for a triangle defined by vertices v1, v2, v3.
            """
            # Create vectors from the vertices
            vec1 = v2 - v1
            vec2 = v3 - v1

            # Calculate the cross product
            normal = np.cross(vec1, vec2)

            # Normalize the vector
            norm = np.linalg.norm(normal)
            if norm == 0:
                return normal
            return normal / norm

        with open(filename, 'w') as file:
            # Write vertices
            vertices = []
            for i in range(lon.shape[0]):
                for j in range(lon.shape[1]):
                    vertex = np.array([self.transformM.get_x(lon[i, j]), 
                                       elevation[i, j], 
                                       -self.transformM.get_y(lat[i, j])])
                    vertices.append(vertex)
                    file.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")

            # Write faces
            normal_index = 1  # Start normal indexing from 1
            for i in range(lon.shape[0] - 1):
                for j in range(lon.shape[1] - 1):
                    # Vertices are 1-indexed in OBJ files
                    v1 = i * lon.shape[1] + j + 1
                    v2 = v1 + 1
                    v3 = v1 + lon.shape[1]
                    v4 = v3 + 1

                    # Define two triangular faces for each square grid
                    #file.write(f"f {v1} {v2} {v4}\n")
                    #file.write(f"f {v1} {v4} {v3}\n")

                    normal1 = calculate_normal(vertices[v1 - 1], vertices[v2 - 1], vertices[v4 - 1])
                    normal2 = calculate_normal(vertices[v1 - 1], vertices[v4 - 1], vertices[v3 - 1])

                    file.write(f"vn {normal1[0]} {normal1[1]} {normal1[2]}\n")
                    file.write(f"vn {normal2[0]} {normal2[1]} {normal2[2]}\n")

                    file.write(f"f {v1}//{normal_index} {v2}//{normal_index} {v4}//{normal_index}\n")
                    normal_index += 1
                    file.write(f"f {v1}//{normal_index} {v4}//{normal_index} {v3}//{normal_index}\n")
                    normal_index += 1
    
    def bilinear_interpolate(self, lon, lat):
        x_pixel, y_pixel = self.latlon_to_pixel(lon, lat, self.dataset)
        x_pixel, y_pixel = x_pixel - self.bounds[0][0], y_pixel - self.bounds[0][1]

        # Find the four surrounding grid points
        x1, y1 = int(x_pixel), int(y_pixel)
        x2, y2 = x1 + 1, y1 + 1

        # Check if the point is within the data bounds
        rows, cols = self.dem_subset.shape
        if x1 >= cols or x2 < 0 or y1 >= rows or y2 < 0:
            return 0  # Point is outside the data bounds

        # Get the elevations of the four surrounding grid points
        Q11 = self.dem_subset[y1, x1]
        Q21 = self.dem_subset[y1, x2] if x2 < cols else Q11
        Q12 = self.dem_subset[y2, x1] if y2 < rows else Q11
        Q22 = self.dem_subset[y2, x2] if x2 < cols and y2 < rows else Q11

        #print(Q11, Q12, Q21, Q22)

        # Interpolate along x for the two pairs of points
        fxy1 = (x2 - x_pixel) / (x2 - x1) * Q11 + (x_pixel - x1) / (x2 - x1) * Q21
        fxy2 = (x2 - x_pixel) / (x2 - x1) * Q12 + (x_pixel - x1) / (x2 - x1) * Q22
        #print(x_pixel, y_pixel, x1, y1, x2, y2)

        # Interpolate along y
        fxy = (y2 - y_pixel) / (y2 - y1) * fxy1 + (y_pixel - y1) / (y2 - y1) * fxy2

        return fxy

    # Convert pixel coordinates to latitude and longitude
    def pixel_to_latlon(self, x, y, geo_transform, transform):
        x_geo = geo_transform[0] + x * geo_transform[1] + y * geo_transform[2]
        y_geo = geo_transform[3] + x * geo_transform[4] + y * geo_transform[5]
        lat, lon, _ = transform.TransformPoint(x_geo, y_geo)
        return lon, lat


def calculate_elevation(x, y, z, Elevator):
    #print(x, y, z)
    lon = Elevator.transformM.get_lon(x)
    lat = Elevator.transformM.get_lat(-z)
    # print(f"lon = {lon}, lat = {lat}")
    elevation = Elevator.bilinear_interpolate(lon, lat)
    # print(f"elevation = {elevation}")
    #return y + 10  # Example: increase y by 10
    return y + elevation


def process_obj_file(file_path, Elevator):
    # Read the .obj file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    new_lines = []
    skip = False  # Flag to indicate skipping lines

    for line in lines:
        if 'g SurfaceArea' in line:
            skip = True  # Set the flag to skip subsequent lines
            continue  # Skip the current line

        if skip:
            continue  # Skip all lines after 'g SurfaceArea'

        # Check if the line defines a vertex
        if line.startswith('v '):
            parts = line.split()
            # Assume the format is: v x y z
            x, y, z = map(float, parts[1:4])
            # Modify the y-coordinate
            y = calculate_elevation(x, y, z, Elevator)
            new_line = f'v {x} {y} {z}\n'
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    # Write the updated content back to the .obj file
    with open(file_path, 'w') as file:
        file.writelines(new_lines)


def elevate(filename, Elevator):
    process_obj_file(filename, Elevator)