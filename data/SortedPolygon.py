__author__ = 'Nikita.Tolstikov'
from Polygon import Polygon
from SortedPoint import SortedPoint

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
        self.__max_x = self.points[0].x
        self.__max_y = self.points[0].y
        self.__min_x = self.points[0].x
        self.__min_y = self.points[0].y
        for p in self.points:
            if self.__max_y < p.y:
                self.__max_y = p.y
            if self.__min_y > p.y:
                self.__min_y = p.y
            if self.__max_x < p.x:
                self.__max_x = p.x
            if self.__min_x > p.x:
                self.__min_x = p.x

    def get_max_y(self):
        return self.__max_y

    def get_min_y(self):
        return self.__min_y

    def get_max_x(self):
        return self.__max_x

    def get_min_x(self):
        return self.__min_x

    min_y = property(get_min_y)
    max_y = property(get_max_y)
    min_x = property(get_min_x)
    max_x = property(get_max_x)

    def get_sorted_points(self):
        if self.__sorted_points is not None:
            return self.__sorted_points
        self.__sorted_points = [SortedPoint(point.x, point.y, self.__id) for point in self.points]
        self.__sorted_points.sort(key = SortedPoint.get_x)

        leftx = self.__sorted_points[0].x
        i = 0
        while leftx == self.__sorted_points[i].x:
            self.__sorted_points[i].is_first = True
            i += 1

        self.__sorted_points[-1].is_last = True
        return self.__sorted_points
