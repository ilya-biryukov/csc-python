__author__ = 'Nikita.Tolstikov'
from Polygon import Polygon
from SortedPoint import SortedPoint
from Point import Point

class SortedPolygon(Polygon):
    def __init__(self, points, polygon_id):
        Polygon.__init__(self, points)
        self.__id = polygon_id
        self.__get_extreme_point()
        self.__sorted_points = None

    def get_polygon_id(self):
        return self.__id

    id = property(get_polygon_id)

    def __get_extreme_point(self):
        self.__max_y = self.points[0].y
        self.__min_y = self.points[0].y
        for p in self.points:
            if self.__max_y < p.y:
                self.__max_y = p.y
            if self.__min_y > p.y:
                self.__min_y = p.y

    def get_max_y(self):
        return self.__max_y

    def get_min_y(self):
        return self.__min_y

    min_y = property(get_min_y)
    max_y = property(get_max_y)

    def get_sorted_points(self):
        if not self.__sorted_points is None:
            return self.__sorted_points
        self.__sorted_points = []
        for point in self.points:
            self.__sorted_points.append(SortedPoint(point.x, point.y, self.__id))
        self.__sorted_points = sorted(self.__sorted_points, key = lambda point: point.x)

        leftx = self.__sorted_points[0].x
        i = 0
        while leftx == self.__sorted_points[i].x:
            self.__sorted_points[i].is_first = True
            i += 1

        self.__sorted_points[-1].is_last = True
        return self.__sorted_points
