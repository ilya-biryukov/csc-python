__author__ = 'Nikita.Tolstikov'

from Point import Point
import string

class SortedPoint(Point):
    def __init__(self, coordinates, polygon_id, is_first = False, is_last = False):
        Point.__init__(self, coordinates)
        self.__polygon_id = polygon_id
        self.__is_first = is_first
        self.__is_last = is_last

    def __init__(self, x, y, polygon_id, is_first = False, is_last = False):
        Point.__init__(self, [x,y])
        self.__polygon_id = polygon_id
        self.__is_first = is_first
        self.__is_last = is_last

    def get_polygon_id(self):
        return self.__polygon_id

    def get_is_first(self):
        return self.__is_first

    def set_is_first(self, is_first):
        self.__is_first = is_first

    def get_is_last(self):
        return self.__is_last

    def set_is_last(self, is_last):
        self.__is_last = is_last

    def __str__(self):
        return '({0:f};{1:f}):{2:d}'.format(self.x ,self.y, self.pid)

    def __eq__(self, other):
        if isinstance(other,Point):
            return Point.__eq__(self, other)
        return Point.__eq__(self, other) and self.pid == other.pid

    is_first = property(get_is_first, set_is_first)
    is_last = property(get_is_last, set_is_last)
    pid = property(get_polygon_id)