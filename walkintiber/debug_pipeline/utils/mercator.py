import math

class Mercator():
    def __init__(self, av_lon_lat=[12.47526999999999, 41.89109000000002]):
        self.R =  6378137.0
        Olon = av_lon_lat[0]#12.47526999999999
        Olat = av_lon_lat[1]#41.89109000000002
        self.scaleFactor = self.earthCircumference(Olat)
        self.originY = self.lat2y(Olat) * self.scaleFactor
        self.originX = self.lon2x(Olon) * self.scaleFactor
        print(f"OX = {self.originX}, OY = {self.originY}")

    def y2lat(self, y):
        #return math.degrees(2 * math.atan(math.exp (y / self.R)) - math.pi / 2.0)
        return 360.0 * math.atan(math.exp((y - 0.5) * (2.0 * math.pi))) / math.pi - 90.0;
    def lat2y(self, lat):
        sinLat = math.sin(math.radians(lat));
        return math.log((1.0 + sinLat) / (1.0 - sinLat)) / (4.0 * math.pi) + 0.5
    def x2lon(self, x):
        return 360.0*(x-0.5)
    def lon2x(self, lon):
        return (lon + 180.0) / 360.0
    def earthCircumference(self,lat):
        EC = 40075016.686
        return EC * math.cos(math.radians(lat))
    
    def get_x(self, lon):
        return self.lon2x(lon) * self.scaleFactor - self.originX
    
    def get_y(self, lat):
        return self.lat2y(lat) * self.scaleFactor - self.originY
    
    def get_lat(self, y):
        return self.y2lat((y + self.originY)/self.scaleFactor)
    
    def get_lon(self, x):
        return self.x2lon((x + self.originX)/self.scaleFactor)