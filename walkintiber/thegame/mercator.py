import math

class Mercator():
    def __init__(self):
        self.R =  6378137.0
        Olat = 41.89109000000002
        Olon = 12.47526999999999
        self.scaleFactor = self.earthCircumference(Olat)
        self.originY = self.lat2y(Olat) * self.scaleFactor
        self.originX = self.lon2x(Olon) * self.scaleFactor

    def y2lat(self, y):
        return math.degrees(2 * math.atan(math.exp (y / R)) - math.pi / 2.0)
    def lat2y(self, lat):
        sinLat = math.sin(math.radians(lat));
        return math.log((1.0 + sinLat) / (1.0 - sinLat)) / (4.0 * math.pi) + 0.5
    def x2lng(self, x):
        return math.degrees(x / self.R)
    def lon2x(self, lon):
        return (lon + 180.0) / 360.0
    def earthCircumference(self,lat):
        EC = 40075016.686
        return EC * math.cos(math.radians(lat))
    
    def get_x(self, lon):
        return self.lon2x(lon) * self.scaleFactor - self.originX
    
    def get_y(self, lat):
        return self.lat2y(lat) * self.scaleFactor - self.originY