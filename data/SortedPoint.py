__author__ = 'Nikita.Tolstikov'

from Point import Point

class SortedPoint(Point):
    def __init__(self, coordinates, polygon_id, is_first = False, is_last = False):
        Point.__init__(self, coordinates)
        self.__polygon_id = polygon_id
        self.__is_first = is_first
        self.__is_last = is_last

    def __init__(self, point, polygon_id, is_first = False, is_last = False):
        Point.__init__(self, [point.x, point.y])
        self.__polygon_id = polygon_id
        self.__is_first = is_first
        self.__is_last = is_last

    def get_is_first(self):
        return self.__is_first

    def set_is_first(self, is_first):
        self.__is_first = is_first

    def get_is_last(self):
        return self.__is_last

    def set_is_last(self, is_last):
        self.__is_last = is_last

    is_first = property(get_is_first, set_is_first)
    is_last = property(get_is_last, set_is_last)
