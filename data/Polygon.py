from Point import Point

class Polygon(object):
    def __init__(self, points):
        """ Initialize polygon with a list of (float, float) pairs --- points of its' vertices
        """
        self.__points = [Point(p[0], p[1]) for p in points]

    def get_points(self):
        return self.__points

    points = property(get_points)


